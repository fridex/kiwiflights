#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ####################################################################
# Copyright (C) 2016  Fridolin Pokorny, fridex.devel@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################

import os
import pytest
import json
from kiwiflights import System

_TESTCASE_COUNT = 10
_ERRORCASE_COUNT = 4
_TEST_INPUT_DIR = os.path.join('test', 'input')
_TEST_OUTPUT_DIR = os.path.join('test', 'output')


class TestSimple(object):
    @pytest.mark.parametrize("input_file",
                             ["testcase_%02d.csv" % i for i in range(1, _TESTCASE_COUNT + 1)])
    def test_testcase(self, input_file):
        with open(os.path.join(_TEST_INPUT_DIR, input_file), 'r') as f:
            system = System.from_csv_file(f)

        itineraries_raw = system.compute_itineraries()
        itineraries = [i.to_dict() for i in itineraries_raw]

        with open(os.path.join(_TEST_OUTPUT_DIR, input_file + ".json"), 'r') as f:
            reference = json.load(f)

        # we encapsulate list of itineraries to dict in CLI so dereference reference
        assert itineraries == reference['itineraries']

    @pytest.mark.parametrize("input_file",
                             ["errorcase_%02d.csv" % i for i in range(1, _ERRORCASE_COUNT + 1)])
    def test_errorcase(self, input_file):
        with open(os.path.join(_TEST_INPUT_DIR, input_file), 'r') as f:
            with pytest.raises(ValueError):
                System.from_csv_file(f)
