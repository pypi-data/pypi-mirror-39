#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytorchtools` package."""

import os
import re
import unittest

from pytorchtools import pytorchtools
from pytorchtools import __version__

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE_PATH = os.path.join(ROOT_DIR, 'pytorchtools', '__init__.py')


class TestPytorchtools(unittest.TestCase):
    """Tests for `pytorchtools` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_version(self):
        """Test version."""
        file_version = ''
        version = __version__
        print("opening {}".format(VERSION_FILE_PATH))
        with open(VERSION_FILE_PATH, "r") as file:
            for line in file:
                if line.startswith('__version__'):
                    file_version = line.split('=')[1].lstrip().replace("'", "").replace("\n", "")

                    break
        assert file_version == version, "file version {} does not match version {}".format(file_version, version)
        print("Version to release {}".format(version))
