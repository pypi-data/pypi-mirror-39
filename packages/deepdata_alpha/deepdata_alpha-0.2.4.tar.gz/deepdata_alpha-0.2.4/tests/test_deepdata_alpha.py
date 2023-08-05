#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the deepdata_alpha module.
"""
import pytest

from deepdata_alpha import deepdata_alpha


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_deepdata_alpha(an_object):
    assert an_object == {}
