#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `slugifile` package."""

import pytest

from click.testing import CliRunner

from slugifile import slugifile
from slugifile import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for slugifile.' in help_result.output
