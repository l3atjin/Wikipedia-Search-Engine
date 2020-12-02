"""Autograder utilities."""
import shutil
import pathlib
import collections
import pytest
import bs4
from .cd import CD
from .pipeline import Pipeline
from .hadoop import hadoop


# Directory containing unit tests.  Tests look here for files like inputs.
TEST_DIR = pathlib.Path(__file__).parent.parent

# Default timeout to wait for student code to respond
TIMEOUT = 10

# Tolerance for comparing IDF and normalization values
EPSILON = 0.05


def create_and_clean_testdir(tmpdir, basename):
    """Remove tmpdir/basename and then create it."""
    dirname = pathlib.Path(tmpdir)/basename
    if dirname.exists():
        shutil.rmtree(dirname)
    dirname.mkdir(exist_ok=True, parents=True)
    return dirname


def create_and_clean_pipeline_testdir(tmpdir, basename):
    """Copy map and reduce executables and stopwords into clean tmp dir."""
    tmpdir = create_and_clean_testdir(tmpdir, basename)
    inverted_index_dir = pathlib.Path("hadoop/inverted_index")
    for filename in inverted_index_dir.glob("map?.py"):
        shutil.copy(filename, tmpdir)
    for filename in inverted_index_dir.glob("reduce?.py"):
        shutil.copy(filename, tmpdir)
    shutil.copy("index/index/stopwords.txt", tmpdir)
    return tmpdir


def threesome(iterable):
    """Organize a list in groups of 3.

    Example:
    >>> list(threesome([1, 2, 3, 4, 5, 6]))
    [(1, 2, 3), (4, 5, 6)]

    """
    assert len(list(iterable)) % 3 == 0, "length must be a multiple of 3"
    return zip(*(iter(iterable),) * 3)


def parse_inverted_index_line(line):
    """Return term, doc_id, dict of norms occurrences and dict of norms."""
    elts = line.strip().split()

    # Term and IDF are first two values
    term = elts[0]
    idf = float(elts[1])

    # Remaining elements are in groups of three: doc_id, number of occurrences,
    # and normalization factor.
    Doc = collections.namedtuple("Doc", ["occurrences", "norm"])
    docs = {}
    for doc_id, occurrences, norm in threesome(elts[2:]):
        docs[doc_id] = Doc(int(occurrences), float(norm))

    return term, idf, docs


def assert_compare_inverted_indexes(path1, path2):
    """Compare two inverted index files, raising an assertion if different."""
    # Read files into memory
    with path1.open() as infile:
        inverted_index1 = infile.readlines()
    with path2.open() as infile:
        inverted_index2 = infile.readlines()

    # Inverted indexes may not be in sorted order.  Sort them so we can compare
    # line-by-line.
    inverted_index1 = sorted(inverted_index1)
    inverted_index2 = sorted(inverted_index2)

    # Verify correct number of terms
    assert len(inverted_index1) == len(inverted_index2)

    # Compare list of documents for each term.  One line of the inverted index
    # may contain multiple documents.  One document is represented by 3
    # numbers: doc id, number of occurrences of the term, and normalization
    # factor.
    for line1, line2 in zip(inverted_index1, inverted_index2):
        term1, idf1, docs1 = parse_inverted_index_line(line1)
        term2, idf2, docs2 = parse_inverted_index_line(line2)

        # Verify terms and IDF values match
        assert term1 == term2, "Term mismatch: '{term}'".format(term=term1)
        assert idf1 == pytest.approx(idf2, EPSILON), \
            "IDF mismatch term '{term}'".format(term=term1)

        # Verify number of occurrences and normalization factors
        assert docs1.keys() == docs2.keys(), \
            "Doc ID mismatch term '{term}': {doc_ids1} != {doc_ids2}".format(
                term=term1,
                doc_ids1=docs1.keys(),
                doc_ids2=docs2.keys(),
            )

        # Verify number of occurrences and normalization factor for each hit
        for doc_id in docs1:
            assert docs1[doc_id].occurrences == docs2[doc_id].occurrences, \
                "Occurrences mismatch term '{term}': {occ1} != {occ2}".format(
                    term=term1,
                    occ1=docs1[doc_id].occurrences,
                    occ2=docs2[doc_id].occurrences,
                )
            assert docs1[doc_id].norm == \
                pytest.approx(docs2[doc_id].norm, EPSILON), \
                "Norm mismatch term '{term}': {norm1} != {norm2}".format(
                    term=term1,
                    norm1=docs1[doc_id].norm,
                    norm2=docs2[doc_id].norm,
                )
