import argparse

import pytest

import arguable.base
import arguable.parser


@pytest.fixture
def mock_sys_argv_help(mocker):
    return mocker.patch('sys.argv', ['', '--help'])


@pytest.fixture
def mock_sys_exit(mocker):
    return mocker.patch('sys.exit')


@pytest.fixture(scope='function')
def mock_arguable_super_parser(mocker):
    return mocker.patch(
        'arguable.base.Arguable.super_parser',
        argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter))


def test_full_help_parser(capsys, mock_sys_argv_help, mock_sys_exit, mock_arguable_super_parser):
    class TestA(arguable.base.Arguable):
        config = argparse.Namespace(x=1)

    class TestB(arguable.base.Arguable):
        config = argparse.Namespace(y=2)

    parser = arguable.parser.FullHelpParser()
    parser.parse_args()

    help_text = capsys.readouterr().out

    assert '--testa-x' in help_text
    assert '--testb-y' in help_text
    assert 'X (default: 1)' in help_text
    assert 'Y (default: 2)' in help_text
    assert mock_sys_exit.call_args == ((0,), {})
