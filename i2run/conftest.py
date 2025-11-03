import os
import sys
import django
import pytest
from pathlib import Path
from pytest import fixture

# Add server directory and project root to Python path
server_path = Path(__file__).parent.parent / "server"
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(server_path))
sys.path.insert(0, str(project_root))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccp4x.config.settings")

# Set up test projects directory
TEST_PROJECTS_DIR = Path(__file__).parent / "test_projects"
os.environ["CCP4I2_PROJECTS_DIR"] = str(TEST_PROJECTS_DIR)

# Initialize Django
django.setup()

# Import from i2run package using absolute imports
from i2run.urls import pdbe_fasta, redo_cif, redo_mtz, rcsb_mmcif
from i2run.utils import download


def pytest_collection_modifyitems(items):
    """Automatically add django_db marker to all test items."""
    for item in items:
        item.add_marker(pytest.mark.django_db(transaction=True))


@fixture(scope="session")
def test_projects_dir():
    """Create and return test projects directory."""
    TEST_PROJECTS_DIR.mkdir(exist_ok=True)
    yield TEST_PROJECTS_DIR
    # Don't clean up - leave for inspection


@fixture(scope="session", autouse=True)
def django_db_setup(django_db_blocker):
    """Set up test database for Django. Auto-use ensures it runs for all tests."""
    from django.core.management import call_command
    from django.conf import settings

    # Use a test-specific database in test_projects directory
    test_db_path = TEST_PROJECTS_DIR / "test_ccp4x.sqlite"
    settings.DATABASES['default']['NAME'] = str(test_db_path)

    # Also set CCP4I2_PROJECTS_DIR in settings to match our test directory
    settings.CCP4I2_PROJECTS_DIR = TEST_PROJECTS_DIR

    # Unblock database access for migrations
    with django_db_blocker.unblock():
        # Create tables
        call_command('migrate', '--run-syncdb', verbosity=0)

    yield

    # Don't clean up database - leave for inspection


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
