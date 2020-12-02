"""Shared test fixtures.

Pytest fixture docs:
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""

import time
import shutil
from pathlib import Path
import logging
from urllib.parse import urljoin
import socket
import urllib
import threading
import flask
import requests
import pytest
import utils
import index
import search


# Set up logging
LOGGER = logging.getLogger("autograder")

# How long to wait for server in separate thread to start or stop
SERVER_START_STOP_TIMEOUT = 5


@pytest.fixture(name='search_app')
def setup_teardown_search_app():
    """Configure a search Flask app object to be used as a live server."""
    LOGGER.info("Setup test fixture 'search_app'")

    # Reset wikipedia database
    db_path = Path("search/search/var/wikipedia.sqlite3")
    db_path.parent.mkdir(exist_ok=True)
    shutil.copy(
        utils.TEST_DIR/"testdata/wikipedia.sqlite3",
        db_path,
    )

    # Configure Flask app.  Testing mode so that exceptions are propagated
    # rather than handled by the the app's error handlers.
    search.app.config["TESTING"] = True

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    yield search.app

    # Teardown code starts here
    LOGGER.info("Teardown test fixture 'search_app'")


@pytest.fixture(name='index_app')
def setup_teardown_index_app():
    """Configure a index Flask app object to be used as a live server."""
    LOGGER.info("Setup test fixture 'index_app'")

    # Reset the database
    assert Path("index/index/inverted_index.txt").exists()

    # Configure Flask app.  Testing mode so that exceptions are propagated
    # rather than handled by the the app's error handlers.
    index.app.config["TESTING"] = True

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    yield index.app

    # Teardown code starts here
    LOGGER.info("Teardown test fixture 'index_app'")


@pytest.fixture(name='search_client')
def search_client_setup_teardown(index_app, search_app):
    """Start app in a separate process."""
    LOGGER.info("Setup test fixture 'live_server'")

    # Start inverted index REST API server.  Port selection is automatic.
    live_server_index = LiveServer(index_app)
    live_server_index.start()
    index_api_url = urljoin(live_server_index.url(), "/api/v1/hits/")
    response = requests.get(urljoin(live_server_index.url(), "/api/v1/"))
    assert response.status_code == 200, "Index server is not up"

    # Start search server, configured to connect to inverted index server port.
    # Port selection for search server is automatic.
    assert "INDEX_API_URL" in search_app.config
    search_app.config["INDEX_API_URL"] = index_api_url

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    with search.app.test_client() as client:
        yield client

    # Stop server
    LOGGER.info("Teardown test fixture 'live_server'")
    live_server_index.stop()


@pytest.fixture(name="index_client")
def client_setup_teardown():
    """
    Start a Flask test server with a clean database.

    This fixture is used to test the REST API, it won't start a live server.

    Flask docs: https://flask.palletsprojects.com/en/1.1.x/testing/#testing
    """
    LOGGER.info("Setup test fixture 'client'")

    # Configure Flask test server
    index.app.config["TESTING"] = True

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    with index.app.test_client() as client:
        yield client

    # Teardown code starts here
    LOGGER.info("Teardown test fixture 'client'")


class LiveServer:
    """Represent a Flask app running in a separate thread."""

    def __init__(self, app, port=None):
        """Find an open port and create a thread object."""
        self.app = app
        self.port = self.get_open_port() if port is None else port

        def shutdown_server():
            """Shut down Flask's underlying Werkzeug WSGI server."""
            shutdown_func = flask.request.environ.get(
                "werkzeug.server.shutdown"
            )
            if shutdown_func is None:
                raise RuntimeError("Not running with a Werkzeug Server.")
            shutdown_func()
            return "Shutting down live server..."

        # Monkey-patch Flask app with a shutdown route at runtime.
        # This is required since threads do not have an elegant method for
        # terminating execution (e.g. a programatic ctrl+c to end the server).
        # More info: https://stackoverflow.com/a/17053522/3820660
        if "shutdown" not in self.app.view_functions:
            self.app.add_url_rule(
                "/shutdown/",
                endpoint="shutdown",
                view_func=shutdown_server,
                methods=["POST"]
            )

        # Run Flask app in a new thread. Debug mode, code reloading, and
        # threaded mode are disabled to prevent potential bugs.
        # Run thread in daemon mode to ensure that the thread is killed
        # when the main Python program exits (e.g. in the case of a test
        # failure, uncaught exception, or premature exit)
        self.thread = threading.Thread(
            target=self.app.run,
            name="LiveServer",
            kwargs=({
                "port": self.port,
                "debug": False,
                "use_reloader": False,
                "threaded": False,
            }),
            daemon=True
        )

    def url(self):
        """Return base URL of running server."""
        return "http://localhost:{port}/".format(port=self.port)

    def start(self):
        """Start server."""
        self.thread.start()
        assert self.wait_for_urlopen()

    def stop(self):
        """Stop server."""
        shutdown_url = urllib.parse.urljoin(self.url(), "/shutdown/")
        requests.post(shutdown_url)
        # Attempt to join with the main thread until the specified timeout.
        # If the LiveServer thread fails to join with the main thread
        # (e.g. join times out), we will leave the shutdown and cleanup
        # duties to the daemon thread when the Python process exits.
        self.thread.join(timeout=SERVER_START_STOP_TIMEOUT)

    @staticmethod
    def get_open_port():
        """Return a port that is available for use on localhost."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', 0))
            port = sock.getsockname()[1]
        return port

    def wait_for_urlopen(self):
        """Call urlopen() in a loop, returning False if it times out."""
        for _ in range(SERVER_START_STOP_TIMEOUT):
            try:
                urllib.request.urlopen(self.url())
                return True
            except urllib.error.HTTPError as err:
                # HTTP 404 and friends indicate a working server
                if err.code < 500:
                    return True
            except urllib.error.URLError:
                pass
            time.sleep(1)
        return False
