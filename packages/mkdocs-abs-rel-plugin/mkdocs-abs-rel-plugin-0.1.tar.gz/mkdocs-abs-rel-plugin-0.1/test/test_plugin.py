"""Sometimes markdown files have internal absolute links.
This is not advised. This tool converts these absolute links to
relative ones."""

from pathlib import Path

import pytest

from mkdocs_abs_rel_plugin import _absolute_to_rel

DOCUMENT_FOLDER = Path("c:/temp/docs")


@pytest.fixture
def abs_link():
    return "[abs link](/imgs/img.png)"


@pytest.fixture
def abs_image():
    return "![abs image](/imgs/img.png)"


@pytest.fixture
def rel_link():
    return "[rel link](imgs/img.png)"


@pytest.fixture
def abs_link_with_note():
    return '[abs_link_with_note](/imgs/img.png "a note")'


@pytest.fixture
def outside_link():
    return "[outside link](https://www.google.com)"


@pytest.fixture
def no_link():
    return "[no link](abc"


def do_test(content, source_path: Path):
    to_rel = _absolute_to_rel(content, source_path, DOCUMENT_FOLDER)
    return to_rel


def test_links(abs_link, abs_image, rel_link, abs_link_with_note, no_link):
    source_path = DOCUMENT_FOLDER.joinpath("source.html")
    assert "[abs link](imgs/img.png)" == do_test(abs_link, source_path)
    assert "![abs image](imgs/img.png)" == do_test(abs_image, source_path)
    assert "[rel link](imgs/img.png)" == do_test(rel_link, source_path)
    assert (
        do_test(abs_link_with_note, source_path)
        == '[abs_link_with_note](imgs/img.png "a note")'
    )
    assert "[no link](abc" == do_test(no_link, source_path)

    source_path = DOCUMENT_FOLDER.joinpath("product/source.html")
    assert "[abs link](../imgs/img.png)" == do_test(abs_link, source_path)
    assert "![abs image](../imgs/img.png)" == do_test(abs_image, source_path)
    assert "[rel link](imgs/img.png)" == do_test(rel_link, source_path)
    assert '[abs_link_with_note](../imgs/img.png "a note")' == do_test(
        abs_link_with_note, source_path
    )
