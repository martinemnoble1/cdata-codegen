from contextlib import contextmanager
from multiprocessing import Process
from os.path import basename, join
from os import environ
from pathlib import Path
from random import choice
from shutil import rmtree
from string import ascii_letters, digits
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse, unquote
from urllib.request import urlopen
from xml.etree import ElementTree as ET
from subprocess import Popen, run, PIPE, CalledProcessError
import gemmi
import sys

# Try to import from legacy ccp4i2 for getCCP4I2Dir, but make it optional
try:
    from ccp4i2.core.CCP4Utils import getCCP4I2Dir
except ImportError:
    # Fallback: use demo_data from current project
    def getCCP4I2Dir():
        return str(Path(__file__).parent.parent)


@contextmanager
def download(url: str):
    """
    Downloads a file from the given URL and saves it to a temporary file.
    Yields a string path to the temporary file.
    Use in a with statement to ensure the file is deleted afterwards.
    """
    urlName = unquote(basename(urlparse(url).path))
    with urlopen(url, timeout=30) as response:
        name = response.headers.get_filename() or urlName
        name = name.strip().replace(" ", "_")
        name = "".join(c for c in name if c.isalnum() or c in "-_.")
        with NamedTemporaryFile(suffix=f"_{name}", delete=False) as temp:
            while chunk := response.read(1_000_000):
                temp.write(chunk)
        path = Path(temp.name).resolve()
        try:
            yield str(path)
        finally:
            path.unlink(missing_ok=True)


@contextmanager
def i2run(args: list[str], project_name: str = None):
    """
    Run a task through modern cdata-codegen ./ccp4i2 CLI with the given arguments,
    check the diagnostic.xml file does not contain any error reports
    and yield a Path object to the job directory (CCP4_JOBS/job_1).
    Use in a with statement and the project will be cleaned up
    as long as an error is not raised.

    Args:
        args: List of arguments starting with task name, followed by task parameters
        project_name: Optional project name (defaults to tmp_<random>).
                     Should reflect the test name for better organization.
    """
    # Generate project name if not provided
    if project_name is None:
        chars = ascii_letters + digits
        project_name = "tmp_" + "".join(choice(chars) for _ in range(10))

    # Check if we're running in test environment with CCP4I2_PROJECTS_DIR set
    projects_dir = environ.get("CCP4I2_PROJECTS_DIR")
    if projects_dir:
        # Test mode: place project in test_projects directory
        project_path = Path(projects_dir) / project_name
    else:
        # Normal mode: place project in current directory
        project_path = Path(project_name)

    # Find the ccp4i2 executable (should be in parent directory)
    ccp4i2_path = Path(__file__).parent.parent / "ccp4i2"
    if not ccp4i2_path.exists():
        raise FileNotFoundError(f"Could not find ccp4i2 executable at {ccp4i2_path}")

    # Use modern CLI: ./ccp4i2 i2run <task_name> --project_name <name> [task args...]
    # args[0] is the task name, args[1:] are the task parameters
    # Note: We don't pass --project_path; it's auto-detected from CCP4I2_PROJECTS_DIR
    cmd = [
        str(ccp4i2_path),
        "i2run",
        args[0],  # task name
        "--project_name", project_name,
    ] + args[1:]  # task parameters (--HKLIN, --SPACEGROUP, etc.)

    # Run the command
    try:
        result = run(cmd, capture_output=True, text=True, check=True)
        print("=== i2run stdout ===")
        print(result.stdout)
        if result.stderr:
            print("=== i2run stderr ===")
            print(result.stderr)
    except CalledProcessError as e:
        print(f"Error running i2run: {e}")
        print(f"=== stdout ===")
        print(e.stdout)
        print(f"=== stderr ===")
        print(e.stderr)
        raise

    directory = project_path / "CCP4_JOBS" / "job_1"

    # Debug: Show what was actually created
    if directory.exists():
        print(f"=== Job directory contents: {directory} ===")
        for item in directory.iterdir():
            print(f"  {item.name}")
    else:
        print(f"WARNING: Job directory does not exist: {directory}")

    # Check diagnostic.xml for errors
    xml_path = directory / "diagnostic.xml"
    if xml_path.exists():
        errors = ET.parse(xml_path).findall(".//errorReport")
        assert len(errors) == 0, f"Error reports found in diagnostic.xml: {errors}"
    else:
        print(f"Warning: diagnostic.xml not found at {xml_path}")

    # Use try-finally to ensure cleanup happens, but store exception
    error_occurred = False
    try:
        yield directory
    except Exception as e:
        error_occurred = True
        print(f"\n!!! Test failed - preserving job directory for inspection: {project_path}")
        raise
    finally:
        # Only clean up if no error occurred
        if not error_occurred:
            rmtree(str(project_path), ignore_errors=True)
            for extension in ("sqlite", "sqlite-shm", "sqlite-wal"):
                Path(f"{project_path}.{extension}").unlink(missing_ok=True)


def demoData(*paths):
    return join(getCCP4I2Dir(), "demo_data", *paths)


def hasLongLigandName(path):
    "Does the structure contains a residue with a name longer than 3 characters?"
    structure = gemmi.read_structure(str(path), format=gemmi.CoorFormat.Mmcif)
    for model in structure:
        for chain in model:
            for residue in chain:
                if len(residue.name) > 3:
                    return True
    return False
