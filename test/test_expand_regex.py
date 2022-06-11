from md2html.core import *


def test_expand_bold():
    content = "hello **there** world"
    expected = "hello <strong>there</strong> world"

    assert expand_bold(content) == expected


def test_expand_bold_multiple():
    content = "hello **there** world **goodbye** world"
    expected = (
        "hello <strong>there</strong> world <strong>goodbye</strong> world"
    )

    assert expand_bold(content) == expected


def test_expand_italics():
    content = "hello *there* world"
    expected = "hello <em>there</em> world"

    assert expand_italics(content) == expected


def test_expand_italics_multiple():
    content = "hello *there* world *goodbye* world"
    expected = "hello <em>there</em> world <em>goodbye</em> world"

    assert expand_italics(content) == expected


def test_expand_code():
    content = "hello `there` world"
    expected = 'hello <code class="hljs">there</code> world'

    assert expand_code(content) == expected


def test_expand_code_multiple():
    content = "hello `there` world `goodbye` world"
    expected = 'hello <code class="hljs">there</code> world <code class="hljs">goodbye</code> world'  # noqa: E501

    assert expand_code(content) == expected


def test_expand_single_link():
    content = "[example.com](https://example.com)"
    expected = '<a href="https://example.com">example.com</a>'

    assert expand_links(content) == expected


def test_expand_multile_links():
    content = "[1](2) [3](4)"
    expected = '<a href="2">1</a> <a href="4">3</a>'

    assert expand_links(content) == expected


def test_expand_footnote_ref():
    content = "abc [^1] def"
    expected = 'abc <a id="footnote-ref-1" href="#footnote-1">[1]</a> def'

    assert expand_footnode_ref(content) == expected


def test_expand_footnote_ref_with_no_eol():
    content = "abc [^1]"
    expected = 'abc <a id="footnote-ref-1" href="#footnote-1">[1]</a>'

    assert expand_footnode_ref(content) == expected


def test_expand_footnote():
    content = "[^1]: abc"
    expected = '<a id="footnote-1" href="#footnote-ref-1">[1]</a>: abc'

    assert expand_footnote(content) == expected
