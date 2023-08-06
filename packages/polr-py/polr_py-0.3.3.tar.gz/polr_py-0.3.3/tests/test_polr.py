#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `polr` package."""


import unittest
from click.testing import CliRunner

from polr import cli


class TestPolr(unittest.TestCase):
    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.polr)
        assert result.exit_code == 0
        assert 'Usage: polr [OPTIONS] COMMAND [ARGS]...' in result.output
        help_result = runner.invoke(cli.polr, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
