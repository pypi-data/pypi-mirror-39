# -*- coding: utf-8 -*-

"""Tests for `hookmeup` package."""
from __future__ import print_function
import sys

import pytest
import hookmeup
from hookmeup.hookmeup import HookMeUpError

@pytest.fixture
def mock_hookmeup(mocker):
    """Mock hookmeup subcommands"""
    mocker.patch('hookmeup.hookmeup.install')
    mocker.patch('hookmeup.hookmeup.post_checkout')

def test_main_install(mock_hookmeup, mocker):
    """Test the entrypoint with the install subcommand."""
    mocker.patch.object(sys, 'argv', ['hookmeup', 'install'])
    hookmeup.main()
    hookmeup.hookmeup.install.assert_called_once()
    assert hookmeup.hookmeup.post_checkout.call_count == 0

def test_install_too_many_args(mock_hookmeup, mocker):
    """Test install with too many arguments"""
    mocker.patch.object(
            sys,
            'argv',
            ['hookmeup', 'post-checkout', '1']
            )
    with pytest.raises(SystemExit):
        hookmeup.main()
    assert hookmeup.hookmeup.post_checkout.call_count == 0
    assert hookmeup.hookmeup.install.call_count == 0

def test_main_post_checkout(mock_hookmeup, mocker):
    """ Test the entrypoint with the post-checkout subcommand and good
    arguments."""
    mocker.patch.object(
            sys,
            'argv',
            ['hookmeup', 'post-checkout', '1', '2', '3']
            )
    hookmeup.main()
    hookmeup.hookmeup.post_checkout.assert_called_once_with(
            {'old': '1', 'new': '2', 'branch_checkout': 3}
            )
    assert hookmeup.hookmeup.install.call_count == 0

def test_pc_too_few_args(mock_hookmeup, mocker):
    """Test post-checkout with too few arguments"""
    mocker.patch.object(
            sys,
            'argv',
            ['hookmeup', 'post-checkout', '1', '2']
            )
    with pytest.raises(SystemExit):
        hookmeup.main()
    assert hookmeup.hookmeup.post_checkout.call_count == 0
    assert hookmeup.hookmeup.install.call_count == 0

def test_pc_too_many_args(mock_hookmeup, mocker):
    """Test post-checkout with too many arguments"""
    mocker.patch.object(
            sys,
            'argv',
            ['hookmeup', 'post-checkout', '1', '2', '3', '4']
            )
    with pytest.raises(SystemExit):
        hookmeup.main()
    assert hookmeup.hookmeup.post_checkout.call_count == 0
    assert hookmeup.hookmeup.install.call_count == 0

def test_no_args(mock_hookmeup, mocker):
    """Test hookmeup called with no arguments"""
    mocker.patch.object(
            sys,
            'argv',
            ['hookmeup']
            )
    with pytest.raises(SystemExit):
        hookmeup.main()
    hookmeup.hookmeup.post_checkout.assert_not_called()
    hookmeup.hookmeup.install.assert_not_called()

def test_error(mocker):
    """Test case where hookmeup throws an exception"""
    mocker.patch(
            'hookmeup.hookmeup.install',
            new=mocker.MagicMock(side_effect=HookMeUpError('test error'))
            )
    mocker.patch.object(sys, 'argv', ['hookmeup', 'install'])
    mocker.patch('hookmeup.print')
    with pytest.raises(SystemExit):
        hookmeup.main()
    hookmeup.hookmeup.install.assert_called_once()
    hookmeup.print.called_with('hookmeup: test error')
