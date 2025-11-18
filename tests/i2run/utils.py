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
        return str(Path(__file__).parent.parent.parent)


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
    Run a task by calling Django management command directly (in-process).

    This runs in the same process as the test, preserving:
    - Django database setup and transactions
    - Test fixtures
    - Environment configuration

    Yields a Path object to the job directory (CCP4_JOBS/job_1).
    Use in a with statement and the project will be cleaned up
    as long as an error is not raised.

    Args:
        args: List of arguments starting with task name, followed by task parameters
        project_name: Optional project name (defaults to derived from test name).
                     Should reflect the test name for better organization.
    """
    # Generate project name if not provided
    if project_name is None:
        # Try to get the current test name from pytest's request context
        # This requires the test to pass request fixture, but we can't access it here
        # Instead, try to get it from the current pytest node
        try:
            import pytest
            # Get the current pytest item (test) being executed
            current_item = pytest.current_test_node if hasattr(pytest, 'current_test_node') else None
            if current_item:
                # Use the same naming logic as conftest.py for consistency
                test_name = current_item.name.replace("[", "_").replace("]", "_").replace("/", "_")
                project_name = f"tmp_{test_name}"
            else:
                # Fallback to inspecting the call stack to find the test function name
                import inspect
                for frame_info in inspect.stack():
                    # Look for a frame with 'test_' in the function name
                    if frame_info.function.startswith('test_'):
                        test_name = frame_info.function
                        project_name = f"tmp_{test_name}"
                        break
        except Exception:
            pass

        # Final fallback: random name
        if project_name is None:
            chars = ascii_letters + digits
            project_name = "tmp_" + "".join(choice(chars) for _ in range(10))
            project_name = project_name.lower()
        
    # Check if we're running in test environment with CCP4I2_PROJECTS_DIR set
    projects_dir = environ.get("CCP4I2_PROJECTS_DIR")
    if projects_dir:
        # Test mode: place project in test_projects directory
        project_path = Path(projects_dir) / project_name
    else:
        # Normal mode: place project in current directory
        project_path = Path(project_name)

    # Build command-line arguments for i2run management command
    # Format: manage.py i2run task_name --project_name foo --param1 val1 --param2 val2
    i2run_argv = ['manage.py', 'i2run', args[0]]  # args[0] is task name
    i2run_argv.extend(['--project_name', project_name])
    i2run_argv.extend(args[1:])  # Add plugin-specific parameters

    # Save original sys.argv
    original_sys_argv = sys.argv

    try:
        # Update sys.argv for the management command parser
        # The i2run command uses sys.argv[2:] directly, so we need to set it properly
        sys.argv = i2run_argv

        # Import and run the i2run command directly (same process, preserves test database)
        from django.core.management import call_command
        from io import StringIO

        # Capture stdout/stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            # Call the management command directly without additional arguments
            # The command will read sys.argv[2:] which we've already set
            call_command(
                'i2run',
                stdout=stdout_capture,
                stderr=stderr_capture
            )

            # Print captured output
            stdout_val = stdout_capture.getvalue()
            stderr_val = stderr_capture.getvalue()
            if stdout_val:
                print("=== i2run stdout ===")
                print(stdout_val)
            if stderr_val:
                print("=== i2run stderr ===")
                print(stderr_val)

        except Exception as e:
            print(f"Error running i2run: {e}")
            print(f"=== stdout ===")
            print(stdout_capture.getvalue())
            print(f"=== stderr ===")
            print(stderr_capture.getvalue())
            raise
        finally:
            # Explicitly close StringIO objects to free file descriptors
            stdout_capture.close()
            stderr_capture.close()

    finally:
        # Restore original sys.argv
        sys.argv = original_sys_argv

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
        # Force garbage collection to release gemmi file handles
        # This helps prevent resource exhaustion in long test runs
        import gc
        gc.collect()
        gc.collect()  # Run twice to catch circular references

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
