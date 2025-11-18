import os
import sys
import django
import pytest
from pathlib import Path
from pytest import fixture

# Add server directory and project root to Python path
server_path = Path(__file__).parent.parent.parent / "server"
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(server_path))
sys.path.insert(0, str(project_root))

# Configure Django settings
# Force use of test_settings even if run_test.sh set ccp4x.config.settings
os.environ["DJANGO_SETTINGS_MODULE"] = "ccp4x.config.test_settings"

# Set up CCP4I2_ROOT for plugin discovery (.def.xml files)
if "CCP4I2_ROOT" not in os.environ:
    os.environ["CCP4I2_ROOT"] = str(project_root)

# Set up test projects directory
TEST_PROJECTS_DIR = Path(__file__).parent / "test_projects"
os.environ["CCP4I2_PROJECTS_DIR"] = str(TEST_PROJECTS_DIR)

# Source CCP4 environment if available
CCP4_SETUP_SCRIPT = "/Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh"
if Path(CCP4_SETUP_SCRIPT).exists():
    import subprocess
    # Source the setup script and export environment variables
    # Use bash to source the script and print all environment variables
    result = subprocess.run(
        f'source {CCP4_SETUP_SCRIPT} && env',
        shell=True,
        executable='/bin/bash',
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        # Parse the environment variables and add to os.environ
        ccp4_vars = {}
        for line in result.stdout.splitlines():
            if '=' in line:
                key, _, value = line.partition('=')
                # Only set CCP4-related variables and PATH to avoid polluting environment
                if key.startswith('CCP4') or key in ['CBIN', 'CLIB', 'CCP4_SCR', 'PATH', 'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH']:
                    ccp4_vars[key] = value

        # Update os.environ with CCP4 variables
        for key, value in ccp4_vars.items():
            os.environ[key] = value

        print(f"CCP4 environment loaded from {CCP4_SETUP_SCRIPT}")
        print(f"  CCP4={os.environ.get('CCP4', 'NOT SET')}")
        print(f"  CBIN={os.environ.get('CBIN', 'NOT SET')}")
        print(f"  PATH includes CBIN: {os.environ.get('CBIN', '') in os.environ.get('PATH', '')}")
    else:
        print(f"Warning: Failed to source CCP4 setup script: {result.stderr}")
else:
    print(f"Warning: CCP4 setup script not found at {CCP4_SETUP_SCRIPT}")

# Initialize Django
django.setup()

# Import from i2run package using absolute imports
from i2run.urls import pdbe_fasta, redo_cif, redo_mtz, rcsb_mmcif
from i2run.utils import download


def pytest_collection_modifyitems(items):
    """Automatically add django_db marker to all test items."""
    for item in items:
        item.add_marker(pytest.mark.django_db(transaction=True))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Hook to capture test results for cleanup decisions."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@fixture(scope="session")
def test_projects_dir():
    """Create and return test projects directory."""
    TEST_PROJECTS_DIR.mkdir(exist_ok=True)
    yield TEST_PROJECTS_DIR
    # Don't clean up - leave for inspection


@fixture(scope="session", autouse=True)
def django_db_setup():
    """Set up test database directory for Django."""
    from django.conf import settings

    # Ensure test projects directory exists
    TEST_PROJECTS_DIR.mkdir(exist_ok=True)

    # Set CCP4I2_PROJECTS_DIR in settings to match our test directory
    settings.CCP4I2_PROJECTS_DIR = TEST_PROJECTS_DIR

    yield

    # Session cleanup: remove old test databases (keep most recent 10)
    old_dbs = sorted(TEST_PROJECTS_DIR.glob("test_*.sqlite*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old_db in old_dbs[10:]:  # Keep newest 10
        try:
            old_db.unlink()
        except Exception as e:
            print(f"Warning: Failed to clean up old database {old_db}: {e}")


@fixture(autouse=True)
def isolated_test_db(request, django_db_blocker, monkeypatch):
    """Create isolated database for each test with proper Django connection management."""
    import shutil
    import gc
    import resource
    from django.core.management import call_command
    from django.conf import settings
    from django.db import connections

    # Monitor file descriptors at test start (for debugging resource leaks)
    try:
        fd_start = len(os.listdir('/dev/fd'))
    except Exception:
        fd_start = None

    # Generate project directory name matching utils.py i2run() naming convention
    # Format: tmp_{test_file}_{test_function}
    # This matches the project directories created by i2run() for consistency
    import inspect
    test_function = None
    test_file = None

    # Walk up the stack to find the test function and file
    for frame_info in inspect.stack():
        if frame_info.function.startswith('test_'):
            test_function = frame_info.function
            # Extract just the test file name without path or extension
            # e.g., /path/to/test_phaser_simple.py -> phaser_simple
            test_file_path = Path(frame_info.filename)
            if test_file_path.stem.startswith('test_'):
                test_file = test_file_path.stem[5:]  # Remove 'test_' prefix
            break

    # Build consistent project name
    if test_function and test_file:
        project_name = f"tmp_{test_file}_{test_function}"
    elif test_function:
        project_name = f"tmp_{test_function}"
    else:
        # Fallback to pytest node name
        test_name = request.node.name.replace("[", "_").replace("]", "_").replace("/", "_")
        project_name = f"tmp_{test_name}"

    # Clean up project name (replace special chars)
    project_name = project_name.replace("[", "_").replace("]", "_").replace("/", "_").replace("::", "_")

    test_project_dir = TEST_PROJECTS_DIR / project_name

    # Create project directory
    test_project_dir.mkdir(exist_ok=True)

    # Place SQLite database inside the project directory
    # This consolidates all test artifacts (CCP4_JOBS + database) in one location
    test_db_path = test_project_dir / "project.sqlite"

    # Close any existing connections to ensure clean slate
    connections.close_all()

    # Store original database configuration
    original_db_settings = settings.DATABASES['default'].copy()

    # Update database configuration for this test
    # Use monkeypatch to ensure settings are properly isolated per-test
    monkeypatch.setitem(settings.DATABASES['default'], 'NAME', str(test_db_path))

    # Unblock database access for migrations
    with django_db_blocker.unblock():
        # Create and migrate the test database
        call_command('migrate', '--run-syncdb', verbosity=0)

    # Run the test
    yield

    # === AGGRESSIVE RESOURCE CLEANUP ===
    # This section addresses resource exhaustion issues that cause
    # order-dependent test failures (e.g., phaser tests failing after 40+ tests)

    # 1. Force garbage collection to release gemmi objects (known to leak file handles)
    gc.collect()
    gc.collect()  # Run twice to catch circular references

    # 2. Close all Django database connections
    with django_db_blocker.unblock():
        connections.close_all()

    # 3. Restore database configuration (monkeypatch will auto-restore on test end, but be explicit)
    settings.DATABASES['default'] = original_db_settings

    # 4. Monitor file descriptor leaks
    if fd_start is not None:
        try:
            fd_end = len(os.listdir('/dev/fd'))
            fd_leaked = fd_end - fd_start
            if fd_leaked > 5:  # Allow small variations
                print(f"⚠️  File descriptor leak detected: {fd_leaked} FDs leaked in {test_name}")
                print(f"   Start: {fd_start} FDs, End: {fd_end} FDs")
        except Exception:
            pass

    # Only remove the project directory if the test passed
    # Keep failed test directories for debugging
    # Note: With consolidated structure, both CCP4_JOBS and database are in the same directory
    test_failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False

    if not test_failed:
        # Test passed - clean up the project directory (includes both CCP4_JOBS and database)
        try:
            shutil.rmtree(test_project_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Failed to clean up test project directory {test_project_dir}: {e}")
    else:
        # Test failed - preserve directory for debugging
        # Directory contains both CCP4_JOBS/job_1 and project.sqlite for inspection
        print(f"Test failed - preserving project directory: {test_project_dir}")

    # Clean up old project directories from previous test runs
    # Keep only the most recent 10 for debugging
    old_dirs = sorted(TEST_PROJECTS_DIR.glob("tmp_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old_dir in old_dirs[10:]:  # Keep newest 10, delete older ones
        try:
            shutil.rmtree(old_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up {old_dir}: {e}")


@fixture(scope="session")
def cif7beq():
    with download(rcsb_mmcif("7beq")) as path:
        yield path


@fixture(scope="session")
def cif8xfm():
    with download(redo_cif("8xfm")) as path:
        yield path


@fixture(scope="session")
def mtz8xfm():
    with download(redo_mtz("8xfm")) as path:
        yield path


@fixture(scope="session")
def mtz7beq():
    with download(redo_mtz("7beq")) as path:
        yield path


@fixture(scope="session")
def seq8xfm():
    with download(pdbe_fasta("8xfm")) as path:
        yield path
