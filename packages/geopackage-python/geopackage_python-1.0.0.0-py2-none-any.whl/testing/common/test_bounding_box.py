#!/usr/bin/python2.7
"""
Copyright (C) 2014 Reinventing Geospatial, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>,
or write to the Free Software Foundation, Inc., 59 Temple Place -
Suite 330, Boston, MA 02111-1307, USA.

Authors:
    Jenifer Cochran, Reinventing Geospatial Inc (RGi)
Date: 2018-11-11
   Requires: sqlite3, argparse
   Optional: Python Imaging Library (PIL or Pillow)
Credits:
  MapProxy imaging functions: http://mapproxy.org
  gdal2mb on github: https://github.com/developmentseed/gdal2mb

Version:
"""
from pytest import raises

from scripts.common.bounding_box import BoundingBox


class TestBoundingBox(object):

    def test_min_x_greater_than_max_x(self):
        with raises(ValueError):
            BoundingBox(min_x=100.0,
                        min_y=0.0,
                        max_x=0.0,
                        max_y=100.0)

    def test_min_y_greater_than_max_y(self):
        with raises(ValueError):
            BoundingBox(min_x=0.0,
                        min_y=100.0,
                        max_x=100.0,
                        max_y=0.0)