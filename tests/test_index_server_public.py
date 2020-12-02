"""Unit tests for REST API."""
import pytest


# Tolerance for hit score match
EPSILON = 0.05


def assert_compare_hits(actual, solution):
    """Compare two lists of hits."""
    # Build a lookup table from the solution docid key -> score value
    solution_dict = {x["docid"]: x["score"] for x in solution}

    # Verify correct docids are returned
    docids_actual = [x["docid"] for x in actual]
    docids_solution = solution_dict.keys()
    assert set(docids_actual) == set(docids_solution)

    # Compare the score for each hit
    for result in actual:
        docid = result["docid"]
        score_actual = result["score"]
        score_solution = solution_dict[docid]
        assert score_actual == pytest.approx(score_solution, EPSILON)


def test_iserver_world_flags_50(index_client):
    """Multiple word query.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Query the REST API
    response = index_client.get("/api/v1/hits/?q=world+flags&w=0.5")
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {"docid": 24764707, "score": 0.017827449729501156},
        {"docid": 19466336, "score": 0.012192424470044354},
        {"docid": 14595509, "score": 0.011999341548308297},
        {"docid": 15538897, "score": 0.0090066084438701},
        {"docid": 1330190, "score": 0.008599574858348901},
        {"docid": 182259, "score": 0.007672497221419921},
        {"docid": 26043929, "score": 0.007085888978633513},
        {"docid": 16266126, "score": 0.006325545919595078},
        {"docid": 2182698, "score": 0.005875802748214444},
        {"docid": 3616717, "score": 0.0052113192730529586},
        {"docid": 3607937, "score": 0.00518698796927859},
        {"docid": 22625, "score": 0.004022733213007523},
        {"docid": 21648, "score": 0.0035060911487181916},
        {"docid": 268997, "score": 0.0033808179884257557},
        {"docid": 836172, "score": 0.003081638265653461},
        {"docid": 3723271, "score": 0.0029058516656391216},
        {"docid": 34750, "score": 0.0028150593191332944},
        {"docid": 27715261, "score": 0.0015765333230352142}
    ]
    assert_compare_hits(hits_actual, hits_solution)


def test_iserver_dillo_spechars_0(index_client):
    """Special characters in query.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Query the REST API
    response = index_client.get("/api/v1/hits/?q=arma@@dillo&w=0")
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {"docid": 96698, "score": 0.05395034663522972},
        {"docid": 12174946, "score": 0.005169961470525449},
        {"docid": 19598782, "score": 0.00419739779085542}
    ]
    assert_compare_hits(hits_actual, hits_solution)


def test_iserver_the_armadillo_0(index_client):
    """Stopwords in query.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Query the REST API
    response = index_client.get("/api/v1/hits/?q=the+armadillo&w=0")
    assert response.status_code == 200

    # Compare actual hits to solution hits
    hits_actual = response.get_json()["hits"]
    hits_solution = [
        {"docid": 96698, "score": 0.05395034663522972},
        {"docid": 12174946, "score": 0.005169961470525449},
        {"docid": 19598782, "score": 0.00419739779085542}
    ]
    assert_compare_hits(hits_actual, hits_solution)


def test_iserver_issued_aaaaaaa_50(index_client):
    """Query term not in inverted index.

    'index_client' is a fixture fuction that provides a Flask test server
    interface. It is implemented in conftest.py and reused by many tests.
    Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    response = index_client.get("/api/v1/hits/?q=issued+aaaaaaa&w=0.5")
    assert response.status_code == 200
    assert response.get_json() == {"hits": []}
