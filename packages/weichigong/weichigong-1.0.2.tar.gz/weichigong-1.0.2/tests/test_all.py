#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weichigong import zconfig

zc = None


def setup_module(module):
    pass


def setup_function(function):
    global zc
    zc = zconfig('localhost', 'testapp', 'dev')
    pass


def test_set_value():
    global zc
    zc.set('a/b/c', 'abc')
    assert zc.get('a/b/c') == 'abc'
