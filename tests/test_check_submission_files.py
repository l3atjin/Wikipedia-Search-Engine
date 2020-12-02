"""Verify submitted files and directories required by the spec."""

from pathlib import Path


def test_check_submission_files():
    """Check for files and directories required by the spec."""
    assert Path("bin").exists()
    assert Path("bin/search").exists()
    assert Path("bin/index").exists()
    assert Path("bin/indexdb").exists()
    assert Path("bin/install").exists()
    assert Path("hadoop/inverted_index/pipeline.sh").exists()
    assert Path("index").exists()
    assert Path("index/index").exists()
    assert Path("index/setup.py").exists()
    assert Path("search").exists()
    assert Path("search/search/sql").exists()
    assert Path("search/search").exists()
    assert Path("search/search/views").exists()
    assert Path("search/setup.py").exists()
