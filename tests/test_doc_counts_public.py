"""Tests the doc counts."""

from pathlib import Path
import shutil
import utils
from utils import TEST_DIR


def test_doc_count_one_mapper():
    """Execute a doc count MapReduce job with one worker."""
    utils.create_and_clean_testdir("tmp", "test_doc_count_one_mapper")

    # Copy executables
    shutil.copy(
        "hadoop/inverted_index/map0.py",
        "tmp/test_doc_count_one_mapper/",
    )
    shutil.copy(
        "hadoop/inverted_index/reduce0.py",
        "tmp/test_doc_count_one_mapper/",
    )

    # Run MapReduce job
    with utils.CD("tmp/test_doc_count_one_mapper"):
        utils.hadoop(
            input_dir=TEST_DIR/"testdata/test_doc_count_one_mapper/input",
            output_dir="output",
            map_exe="./map0.py",
            reduce_exe="./reduce0.py",
        )

    # Verify doc count
    doc_count_path = "tmp/test_doc_count_one_mapper/total_document_count.txt"
    doc_count_str = Path(doc_count_path).read_text()
    doc_count = int(doc_count_str)
    assert doc_count == 3
