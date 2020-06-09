import argparse
import sys  # noqa: F401 (imported but unused)

import pytest

import arguable.base


@pytest.fixture
def mock_parser_add_argument(mocker):
    return mocker.patch('argparse.ArgumentParser.add_argument')


@pytest.fixture
def mock_sys_argv(mocker):
    return mocker.patch('sys.argv', [
        '',
        '--test-str-param', 'abc',
        '--test-int-param', '123',
        '--test-tuple-param', '1', '2', '3',
        '--test-bool-param',
    ])


@pytest.fixture
def mock_arguable_update_parser(mocker):
    return mocker.patch('arguable.base.Arguable.update_parser')


@pytest.fixture
def mock_arguable_super_parser(mocker):
    return mocker.patch('arguable.base.Arguable.super_parser')


def test_config_base_name():
    class Test(arguable.base.Arguable):
        pass

    assert Test.config_base_name() == 'test'


def test_subclassing_create_parser():
    class Test(arguable.base.Arguable):
        pass

    assert hasattr(Test, 'config_parser')


def test_subclassing_update_super_parser(mock_arguable_update_parser):
    class Test(arguable.base.Arguable):
        pass

    args, __ = mock_arguable_update_parser.call_args
    assert arguable.base.Arguable.super_parser is args[0]


def test_subclassing_with_prefix():
    prefix = 'custom_prefix'

    class Test(arguable.base.Arguable, prefix=prefix):
        pass

    assert Test.config_prefix == prefix
    assert Test.config_base_name() == prefix


def test_subclassing_with_removesuffix():
    class TestClass(arguable.base.Arguable, removesuffix='class'):
        pass

    assert TestClass.config_removesuffix == 'class'
    assert TestClass.config_base_name() == 'test'


def test_update_parser(mock_parser_add_argument, mock_arguable_super_parser):
    class Test(arguable.base.Arguable):
        config = argparse.Namespace(str_param='foo')

    args, kwargs = Test.config_parser.add_argument.call_args
    assert ('--test-str-param',) == args
    assert dict(type=str, default='foo', metavar='', help='Str param') == kwargs


def test_bool_parameter(mock_parser_add_argument, mock_arguable_super_parser):
    class Test(arguable.base.Arguable):
        config = argparse.Namespace(bool_param=True)

    __, kwargs = Test.config_parser.add_argument.call_args
    assert dict(action='store_false', help='Bool param') == kwargs


def test_tuple_parameter(mock_parser_add_argument, mock_arguable_super_parser):
    class Test(arguable.base.Arguable):
        config = argparse.Namespace(tuple_param=(1, 2, 3))

    __, kwargs = Test.config_parser.add_argument.call_args
    assert dict(type=int, default=(1, 2, 3), nargs=3, help='Tuple param')


def test_instantiation_parameter_names(mock_sys_argv, mock_arguable_super_parser):
    class Test(arguable.base.Arguable):
        config = argparse.Namespace(str_param='')

    test = Test()

    assert hasattr(test.config, 'str_param')


def test_instantiation_various_parameter_types(mock_sys_argv, mock_arguable_super_parser):
    class Test(arguable.base.Arguable):
        config = argparse.Namespace(
            str_param='',
            int_param=0,
            tuple_param=(0, 0, 0),
            bool_param=False,
        )

    test = Test()

    assert test.config.str_param == 'abc'
    assert test.config.int_param == 123
    assert test.config.tuple_param == [1, 2, 3]
    assert test.config.bool_param
