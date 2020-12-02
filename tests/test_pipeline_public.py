"""Test the student pipeline."""

from pathlib import Path
import utils
from utils import TEST_DIR


def test_pipeline01_num_phases():
    """Check to see there are a reasonable number of phases."""
    with utils.CD("hadoop/inverted_index/"):
        mapper_exes, reducer_exes = utils.Pipeline.get_exes()
    num_mappers = len(mapper_exes)
    num_reducers = len(reducer_exes)
    assert num_mappers > 1, "Must use more than 1 map phase"
    assert num_reducers > 1, "Must use more than 1 reduce phase"


def test_pipeline03_basic():
    """Test no_stopwords_uppercase_or_nonalphanumeric.

    This test is to check if students are getting a basic document No
    stopwords, upppercase letters, numbers, non-alphanumeric characters or
    repeated words are present within this test
    """
    tmpdir = utils.create_and_clean_pipeline_testdir(
        "tmp",
        "test_pipeline03",
    )

    # Set total document count to be 2
    doc_count_filename = tmpdir/"total_document_count.txt"
    Path(doc_count_filename).write_text("2")

    # Start pipeline mapreduce job, with 1 mapper and 1 reducer
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline03/input",
            output_dir="output",
        )

        # Concatenate output files to output.txt
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline03/expected.txt",
    )


def test_pipeline04_uppercase_characters():
    """Test uppercase chars.

    This test checks if students handle upper case characters correctly,
    they should essentially be replaced with lower case characters.  There
    are no stopwords, numbers or non-alphanumeric characters present in
    this test.
    """
    tmpdir = utils.create_and_clean_pipeline_testdir(
        "tmp",
        "test_pipeline04",
    )

    # Set total document count to be 2
    doc_count_filename = tmpdir/"total_document_count.txt"
    Path(doc_count_filename).write_text("2")

    # Run pipeline mapreduce job with 1 mapper and 1 reducer
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline04/input",
            output_dir="output",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline04/expected.txt",
    )

    # Run same job with 3 mappers and 3 reducers
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline04/input_multi",
            output_dir="output_multi",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline04/expected.txt",
    )


def test_pipeline05_uppercase_chars_numbers():
    """Test uppercase chars w numbers.

    This test checks that students are handling numbers correctly, means
    leaving them inside the word they are apart of. This test also contains
    upper case characters. There are no stopwords or non-alphanumeric
    characters present in this test
    """
    tmpdir = utils.create_and_clean_pipeline_testdir(
        "tmp",
        "test_pipeline05",
    )

    # Set total document count to be 2
    doc_count_filename = tmpdir/"total_document_count.txt"
    Path(doc_count_filename).write_text("2")

    # Run pipeline mapreduce job with 1 mapper and 1 reducer
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline05/input",
            output_dir="output",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline05/expected.txt",
    )

    # Rerun with multiple mappers and reducers
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline05/input_multi",
            output_dir="tmp/test_pipeline05/output_multi",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline05/expected.txt",
    )


def test_pipeline06_non_alnum_chars():
    """Test with non alphanumeric chars.

    This test checks that students are handling non-alphanumeric characters
    properly, i.e. removing them from the word. If a word is only
    non-alphanumeric characters then it is not added to the inverted
    index. There are upper case characters and numbers in this test. There
    no stopwords.
    """
    tmpdir = utils.create_and_clean_pipeline_testdir(
        "tmp",
        "test_pipeline06",
    )

    # Set total document count to be 2
    doc_count_filename = tmpdir/"total_document_count.txt"
    Path(doc_count_filename).write_text("2")

    # Run pipeline mapreduce job with 1 mapper and 1 reducer
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline06/input",
            output_dir="output",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline06/expected.txt",
    )

    # Rerun with multiple mappers and reducers
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline06/input_multi",
            output_dir="output_multi",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline06/expected.txt",
    )


def test_pipeline10_word_in_many_documents():
    """Test word occurs in multiple docs.

    This test checks that studnets are properly handling the case of a word
    appearing in multiple documents This will give the inverted index entry
    a longer than chain of document references.
    """
    tmpdir = utils.create_and_clean_pipeline_testdir(
        "tmp",
        "test_pipeline10",
    )

    # Set total document count to be 3
    doc_count_filename = tmpdir/"total_document_count.txt"
    Path(doc_count_filename).write_text("3")

    # Run pipeline mapreduce job with 1 mapper and 1 reducer
    with utils.CD(tmpdir):
        pipeline = utils.Pipeline(
            input_dir=TEST_DIR/"testdata/test_pipeline10/input_multi",
            output_dir="output_multi",
        )
        output_filename = pipeline.get_output_concat()

    # Verify output
    utils.assert_compare_inverted_indexes(
        output_filename,
        TEST_DIR/"testdata/test_pipeline10/expected.txt",
    )
