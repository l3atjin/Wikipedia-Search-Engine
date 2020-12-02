"""Test student created utility scripts."""
import shutil
import time
import subprocess
from pathlib import Path
import pytest
import utils


# Time to wait for server to start
TIMEOUT = 3

# This pylint warning is endemic to pytest.
# pylint: disable=unused-argument


@pytest.fixture(name="setup_teardown")
def setup_teardown_fixture():
    """Set up the test and cleanup after."""
    # Setup code: make sure no stale processes are running
    assert not pgrep("flask")

    # Transfer control to testcase
    yield None

    # Teardown: kill any stale processes
    pkill("flask")
    assert wait_for_stop()


def test_executables(setup_teardown):
    """Verify bin/index, bin/search, bin/indexdb are shell scripts."""
    assert_is_shell_script("bin/install")
    assert_is_shell_script("bin/search")
    assert_is_shell_script("bin/index")
    assert_is_shell_script("bin/indexdb")


def test_install():
    """Verify install script contains the right commands."""
    install_content = Path("bin/install").read_text()
    assert "python3 -m venv" in install_content
    assert "source env/bin/activate" in install_content
    assert "pip install -r search/requirements.txt" in install_content
    assert "pip install -e search" in install_content
    assert "pip install -r index/requirements.txt" in install_content
    assert "pip install -e index" in install_content
    assert "ln -sf ../../tests/utils/hadoop.py hadoop" in install_content


def test_servers_start(setup_teardown):
    """Verify index and search servers start."""
    subprocess.run(["bin/index", "start"], check=True)
    subprocess.run(["bin/search", "start"], check=True)
    assert wait_for_start()


def test_servers_stop(setup_teardown):
    """Verify index and search servers start."""
    # Start servers
    subprocess.run(["bin/index", "start"], check=True)
    subprocess.run(["bin/search", "start"], check=True)
    assert wait_for_start()

    # Stop servers
    subprocess.run(["bin/index", "stop"], check=True)
    subprocess.run(["bin/search", "stop"], check=True)
    assert wait_for_stop()


def test_indexdb_script(setup_teardown):
    """Test the indexdb script."""
    # Create tmp directory containing search/search/sql/wikipedia.sql
    utils.create_and_clean_testdir("tmp", "test_index_db_script")
    Path("tmp/test_index_db_script/search/search/sql").mkdir(parents=True)
    shutil.copy(
        utils.TEST_DIR/"testdata/small.sql",
        "tmp/test_index_db_script/search/search/sql/wikipedia.sql",
    )

    # Run indexdb script inside tmp directory
    indexdb_path = Path("bin/indexdb").resolve()
    subprocess.run(
        [indexdb_path, "reset"],
        cwd="tmp/test_index_db_script",
        check=True,
    )

    # Verify search/search/var/wikipedia.sqlite3 was created
    assert Path(
        "tmp/test_index_db_script/search/search/var/wikipedia.sqlite3"
    ).exists()


def pgrep(pattern):
    """Return list of matching processes."""
    completed_process = subprocess.run(
        ["pgrep", "-f", pattern],
        check=False,  # We'll check the return code manually
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if completed_process.returncode == 0:
        return completed_process.stdout.strip().split("\n")
    return []


def pkill(pattern):
    """Issue a "pkill -f pattern" command, ignoring the exit code."""
    subprocess.run(["pkill", "-f", pattern], check=False)


def assert_is_shell_script(path):
    """Assert path is an executable shell script."""
    path = Path(path)
    assert path.exists()
    output = subprocess.run(
        ["file", path],
        check=True, stdout=subprocess.PIPE, universal_newlines=True,
    ).stdout
    assert "shell script" in output
    assert "executable" in output


def wait_for_start():
    """Wait for two Flask processes to start running."""
    # Need to check for processes twice to make sure that
    # the flask processes doesn't error out but get marked correct
    count = 0
    for _ in range(TIMEOUT):
        if len(pgrep("flask")) == 2:
            count += 1
        if count >= 2:
            return True
        time.sleep(1)
    return False


def wait_for_stop():
    """Wait for Flask servers to stop running."""
    for _ in range(TIMEOUT):
        if not pgrep("flask"):
            return True
    return False
