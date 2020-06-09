from arguable.utils import removeprefix, removesuffix


def test_removeprefix_empty_prefix():
    assert removeprefix('foo', '') == 'foo'


def test_removeprefix_with_prefix():
    assert removeprefix('foo_bar', 'foo_') == 'bar'


def test_removeprefix_without_prefix():
    assert removeprefix('foo_bar', 'bar_') == 'foo_bar'


def test_removesuffix_empty_suffix():
    assert removesuffix('foo', '') == 'foo'


def test_removesuffix_with_suffix():
    assert removesuffix('foo_bar', '_bar') == 'foo'


def test_removesuffix_without_suffix():
    assert removesuffix('foo_bar', '_foo') == 'foo_bar'
