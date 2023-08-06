"""Tests for `qhdl` package."""

import pytest
from pkg_resources import parse_version

import qhdl


def test_valid_version():
    """Check that the package defines a valid __version__"""
    assert parse_version(qhdl.__version__) >= parse_version("0.1.0")
