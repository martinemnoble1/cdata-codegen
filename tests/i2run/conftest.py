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
    from django.core.management import call_command
    from django.conf import settings
    from django.db import connections

    # Generate unique project directory name based on test name
    test_name = request.node.name.replace("[", "_").replace("]", "_").replace("/", "_")
    test_project_name = f"test_{test_name}_{id(request)}"
    test_project_dir = TEST_PROJECTS_DIR / test_project_name

    # Create project directory
    test_project_dir.mkdir(exist_ok=True)

    # Place SQLite database inside the test's project directory
    test_db_path = test_project_dir / f"{test_project_name}.sqlite"

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

    # Clean up: close connections before deleting database file
    with django_db_blocker.unblock():
        connections.close_all()

    # Restore database configuration (monkeypatch will auto-restore on test end, but be explicit)
    settings.DATABASES['default'] = original_db_settings

    # Only remove the test project directory if the test passed
    # Keep failed test directories for debugging
    test_failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False

    if not test_failed:
        # Test passed - clean up the project directory
        try:
            shutil.rmtree(test_project_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Failed to clean up test project directory {test_project_dir}: {e}")
    else:
        # Test failed - preserve directory for debugging
        print(f"Test failed - preserving project directory: {test_project_dir}")

    # Clean up temp project directories created during the test (non-test directories)
    # Keep only the most recent 5 for debugging
    temp_dirs = sorted(TEST_PROJECTS_DIR.glob("tmp_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for temp_dir in temp_dirs[5:]:  # Keep newest 5, delete older ones
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up {temp_dir}: {e}")


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
