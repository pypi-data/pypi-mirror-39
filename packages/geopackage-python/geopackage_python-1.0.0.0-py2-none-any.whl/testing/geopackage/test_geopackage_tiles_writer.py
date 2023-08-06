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
import math
from os import remove
from os.path import join
from sqlite3 import Binary
from tempfile import gettempdir
from uuid import uuid4

import pytest
from pytest import raises

from scripts.common.zoom_times_two import ZoomTimesTwo
from scripts.geopackage.core.geopackage_core import GEOPACKAGE_CONTENTS_TABLE_NAME, \
    GEOPACKAGE_SPATIAL_REFERENCE_SYSTEM_TABLE_NAME, GeoPackageCore
from scripts.geopackage.extensions.geopackage_extensions import GEOPACKAGE_EXTENSIONS_TABLE_NAME, GeoPackageExtensions
from scripts.geopackage.extensions.extension import Extension
from scripts.geopackage.extensions.vector_tiles.geopackage_mapbox_vector_tiles import GeoPackageMapBoxVectorTiles
from scripts.geopackage.extensions.vector_tiles.vector_fields.geopackage_vector_fields import GeoPackageVectorFields
from scripts.geopackage.extensions.vector_tiles.vector_fields.vector_fields_entry import VectorFieldType
from scripts.geopackage.extensions.vector_tiles.vector_layers.geopackage_vector_layers import GeoPackageVectorLayers
from scripts.geopackage.extensions.vector_tiles.vector_tiles_constants import GEOPACKAGE_VECTOR_LAYERS_TABLE_NAME, \
    GEOPACKAGE_VECTOR_FIELDS_TABLE_NAME
from scripts.geopackage.tiles.geopackage_abstract_tiles import GEOPACKAGE_TILE_MATRIX_TABLE_NAME, \
    GEOPACKAGE_TILE_MATRIX_SET_TABLE_NAME
from scripts.geopackage.tiles.geopackage_tiles import GeoPackageTiles
from scripts.geopackage.tiles.tile_data_information import TileDataInformation
from scripts.geopackage.utility.sql_utility import get_database_connection, table_exists
from scripts.packaging.tiles2gpkg_parallel import img_to_buf
from testing.test_tiles2gpkg import make_gpkg
from testing.geopackage.extensions.vector_tiles.test_geopackage_vector_tiles import TestGeoPackageVectorTiles
from scripts.common.bounding_box import BoundingBox
from scripts.geopackage.geopackage_tiles_writer import GeoPackageTilesWriter, TileType
from PIL.Image import new


class TestGeoPackageWriter(object):

    def test_mapbox(self, get_gpkg_file_path):
        tiles_table_name = "My tiles baby"
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name=tiles_table_name,
                                            srs_id=4326,
                                            srs_bounds=BoundingBox(min_x=-180.0,
                                                                   max_x=180.0,
                                                                   min_y=-90.0,
                                                                   max_y=90.0),
                                            tile_scheme=ZoomTimesTwo(base_matrix_width=2, base_matrix_height=1))
        tile_row_expected = 1
        tile_column_expected = 2
        tile_zoom_expected = 3
        gpkg_writer.add_tile(tile_row=tile_row_expected,
                             tile_column=tile_column_expected,
                             tile_zoom=tile_zoom_expected,
                             tile_data=TestGeoPackageVectorTiles.get_mapbox_vector_tile_data())

        TestGeoPackageWriter.assert_all_vector_tiles_tables(gpkg_file_path=gpkg_writer.file_path,
                                                            tiles_table_extension=GeoPackageMapBoxVectorTiles(
                                                                vector_tiles_table_name=tiles_table_name))

        # assert the tile was added properly
        with get_database_connection(gpkg_writer.file_path) as db_conn:
            tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                          table_name=tiles_table_name,
                                                          tile_row=tile_row_expected,
                                                          tile_column=tile_column_expected,
                                                          zoom_level=tile_zoom_expected)
            assert tile_returned == TestGeoPackageVectorTiles.get_mapbox_vector_tile_data()
            # assert fields and layers were added properly

            # check if the mapbox layers and field entries were extracted and added to the layers table
            vector_layer_entries = GeoPackageVectorLayers.get_vector_layer_entries_by_table_name(
                cursor=db_conn.cursor(),
                vector_tiles_table_name
                =tiles_table_name)

            assert len(vector_layer_entries) == 2

            assert any(vector_layer_entry.table_name == tiles_table_name and
                       vector_layer_entry.name == 'AgricultureSrf'
                       for vector_layer_entry
                       in vector_layer_entries)

            assert any(vector_layer_entry.table_name == tiles_table_name and
                       vector_layer_entry.name == 'TransportationGroundCrv'
                       for vector_layer_entry
                       in vector_layer_entries)

            # check the field entries too
            vector_field_entries = GeoPackageVectorFields.get_vector_field_entry_by_values(cursor=db_conn.cursor(),
                                                                                           id=None,
                                                                                           name='Feature ID',
                                                                                           type=VectorFieldType.NUMBER,
                                                                                           layer_id=None)

            assert len(vector_field_entries) == 2
            # assert the tile matrix entry was added
            tile_matrix_returned = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                  tile_table_name=tiles_table_name,
                                                                                  zoom_level=tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned) == 1
            assert tile_matrix_returned[0].table_name == tiles_table_name and \
                   tile_matrix_returned[0].matrix_height == 8 and \
                   tile_matrix_returned[0].matrix_width == 16 and \
                   tile_matrix_returned[0].zoom_level == tile_zoom_expected and \
                   tile_matrix_returned[0].pixel_x_size == 0.0878906250 and \
                   tile_matrix_returned[0].pixel_y_size == 0.0878906250 and \
                   tile_matrix_returned[0].tile_height == 256 and \
                   tile_matrix_returned[0].tile_width == 256

            # assert the tile matrix set entry was added
            tile_matrix_set_returned = GeoPackageTiles.get_tile_matrix_set_entry_by_table_name(cursor=db_conn.cursor(),
                                                                                               table_name=tiles_table_name)
            assert tile_matrix_set_returned.srs_id == 4326 and \
                   tile_matrix_set_returned.min_x == -180.0 and \
                   tile_matrix_set_returned.min_y == -90.0 and \
                   tile_matrix_set_returned.max_x == 180.0 and \
                   tile_matrix_set_returned.max_y == 90.0 and \
                   tile_matrix_set_returned.table_name == tiles_table_name

            # assert the vector tiles table is in the gpkg contents table
            content = GeoPackageCore.get_content_entry_by_table_name(cursor=db_conn.cursor(),
                                                                     table_name=tiles_table_name)
            assert content.table_name == tiles_table_name and \
                   content.srs_id == 4326 and \
                   content.min_x == -180.0 and \
                   content.min_y == -90.0 and \
                   content.max_x == 180.0 and \
                   content.max_y == 90.0 and \
                   content.data_type == "vector-tiles"

    def test_jpeg(self, get_gpkg_file_path):
        data = TestGeoPackageWriter.get_raster_data("jpeg")

        tile_type = GeoPackageTilesWriter.get_tile_type_from_data(tile_data=data)

        assert tile_type == TileType.JPEG

        tiles_table_name = "My raster tiles baby"
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name=tiles_table_name,
                                            srs_id=4326,
                                            srs_bounds=BoundingBox(min_x=-180.0,
                                                                   max_x=180.0,
                                                                   min_y=-90.0,
                                                                   max_y=90.0))

        tile_row_expected = 2
        tile_column_expected = 3
        tile_zoom_expected = 4
        gpkg_writer.add_tile(tile_row=tile_row_expected,
                             tile_column=tile_column_expected,
                             tile_zoom=tile_zoom_expected,
                             tile_data=data)

        TestGeoPackageWriter.assert_all_raster_tiles_tables(gpkg_file_path=gpkg_writer.file_path,
                                                            tiles_table_name=tiles_table_name)

        # assert the tile was added properly
        with get_database_connection(gpkg_writer.file_path) as db_conn:
            tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                          table_name=tiles_table_name,
                                                          tile_row=tile_row_expected,
                                                          tile_column=tile_column_expected,
                                                          zoom_level=tile_zoom_expected)
            assert tile_returned == Binary(data)

            # assert the tile matrix entry was added
            tile_matrix_returned = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                  tile_table_name=tiles_table_name,
                                                                                  zoom_level=tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned) == 1
            assert tile_matrix_returned[0].table_name == tiles_table_name and \
                   tile_matrix_returned[0].matrix_height == 16 and \
                   tile_matrix_returned[0].matrix_width == 16 and \
                   tile_matrix_returned[0].zoom_level == tile_zoom_expected and \
                   tile_matrix_returned[0].pixel_x_size == 0.0878906250 and \
                   tile_matrix_returned[0].pixel_y_size == 0.0439453125 and \
                   tile_matrix_returned[0].tile_height == 256 and \
                   tile_matrix_returned[0].tile_width == 256

            # assert the tile matrix set entry was added
            tile_matrix_set_returned = GeoPackageTiles.get_tile_matrix_set_entry_by_table_name(cursor=db_conn.cursor(),
                                                                                               table_name=tiles_table_name)
            assert tile_matrix_set_returned.srs_id == 4326 and \
                   tile_matrix_set_returned.min_x == -180.0 and \
                   tile_matrix_set_returned.min_y == -90.0 and \
                   tile_matrix_set_returned.max_x == 180.0 and \
                   tile_matrix_set_returned.max_y == 90.0 and \
                   tile_matrix_set_returned.table_name == tiles_table_name

            # assert the vector tiles table is in the gpkg contents table
            content = GeoPackageCore.get_content_entry_by_table_name(cursor=db_conn.cursor(),
                                                                     table_name=tiles_table_name)
            assert content.table_name == tiles_table_name and \
                   content.srs_id == 4326 and \
                   content.min_x == -180.0 and \
                   content.min_y == -90.0 and \
                   content.max_x == 180.0 and \
                   content.max_y == 90.0 and \
                   content.data_type == "tiles"

    def test_png(self, get_gpkg_file_path):
        data = TestGeoPackageWriter.get_raster_data("png")

        tile_type = GeoPackageTilesWriter.get_tile_type_from_data(tile_data=data)

        assert tile_type == TileType.PNG

        tiles_table_name = "My raster tiles baby PNG"
        srs_bounds = BoundingBox(min_x=-20037508.342789244,
                                 max_x=20037508.342789244,
                                 min_y=-20037508.342789244,
                                 max_y=20037508.342789244)

        with GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                   tile_table_name=tiles_table_name,
                                   srs_id=3395,
                                   srs_bounds=srs_bounds) as gpkg_writer:
            tile_row_expected = 2
            tile_column_expected = 3
            tile_zoom_expected = 2
            gpkg_writer.add_tile(tile_row=tile_row_expected,
                                 tile_column=tile_column_expected,
                                 tile_zoom=tile_zoom_expected,
                                 tile_data=data)

        TestGeoPackageWriter.assert_all_raster_tiles_tables(gpkg_file_path=gpkg_writer.file_path,
                                                            tiles_table_name=tiles_table_name)

        # assert the tile was added properly
        with get_database_connection(gpkg_writer.file_path) as db_conn:
            tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                          table_name=tiles_table_name,
                                                          tile_row=tile_row_expected,
                                                          tile_column=tile_column_expected,
                                                          zoom_level=tile_zoom_expected)
            assert tile_returned == Binary(data)

            # assert the tile matrix entry was added
            tile_matrix_returned = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                  tile_table_name=tiles_table_name,
                                                                                  zoom_level=tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned) == 1
            assert tile_matrix_returned[0].table_name == tiles_table_name and \
                   tile_matrix_returned[0].matrix_height == 4 and \
                   tile_matrix_returned[0].matrix_width == 4 and \
                   tile_matrix_returned[0].zoom_level == tile_zoom_expected and \
                   tile_matrix_returned[0].pixel_x_size == 39135.7584820102421875 and \
                   tile_matrix_returned[0].pixel_y_size == 39135.7584820102421875 and \
                   tile_matrix_returned[0].tile_height == 256 and \
                   tile_matrix_returned[0].tile_width == 256

            # assert the tile matrix set entry was added
            tile_matrix_set_returned = GeoPackageTiles.get_tile_matrix_set_entry_by_table_name(cursor=db_conn.cursor(),
                                                                                               table_name=tiles_table_name)
            assert tile_matrix_set_returned.srs_id == 3395 and \
                   tile_matrix_set_returned.min_x == srs_bounds.min_x and \
                   tile_matrix_set_returned.min_y == srs_bounds.min_y and \
                   tile_matrix_set_returned.max_x == srs_bounds.max_x and \
                   tile_matrix_set_returned.max_y == srs_bounds.max_y and \
                   tile_matrix_set_returned.table_name == tiles_table_name

            # assert the vector tiles table is in the gpkg contents table
            content = GeoPackageCore.get_content_entry_by_table_name(cursor=db_conn.cursor(),
                                                                     table_name=tiles_table_name)
            assert content.table_name == tiles_table_name and \
                   content.srs_id == 3395 and \
                   content.min_x == srs_bounds.min_x and \
                   content.min_y == srs_bounds.min_y and \
                   content.max_x == srs_bounds.max_x and \
                   content.max_y == srs_bounds.max_y and \
                   content.data_type == "tiles"

    def test_invalid_gpkg_path(self):
        with raises(ValueError):
            GeoPackageTilesWriter(gpkg_file_path=gettempdir(),
                                  tile_table_name="Richard_Kim",
                                  srs_id=1111,
                                  srs_bounds=BoundingBox(0.0, 0.0, 0.0, 0.0))

    def test_invalid_tile_add_zoom_level_value(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=1234,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_row=0,
                                 tile_column=0,
                                 tile_zoom=-9,
                                 tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

    def test_invalid_tile_add_mix_raster_vector(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=0,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))
        gpkg_writer.add_tile(tile_row=0,
                             tile_column=0,
                             tile_zoom=0,
                             tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=1,
                                 tile_data=TestGeoPackageVectorTiles.get_mapbox_vector_tile_data())

    def test_invalid_tile_add_mix_vector_raster(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=-1,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))
        gpkg_writer.add_tile(tile_row=0,
                             tile_column=0,
                             tile_zoom=0,
                             tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=1,
                                 tile_data=TestGeoPackageVectorTiles.get_mapbox_vector_tile_data())

    def test_invalid_tile_add_bad_data(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=1,
                                 tile_data=Binary(bytes("bad_data".encode('utf-8'))))

    def test_invalid_tile_raster_mime_type(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=1,
                                 tile_data=TestGeoPackageWriter.get_raster_data("gif"))

    def test_invalid_tile_column_value_negative(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=-1,
                                 tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

    def test_invalid_tile_column_value_larger_than_matrix_width(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=1,
                                 tile_column=2,
                                 tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

    def test_invalid_tile_row_value_negative(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=-1,
                                 tile_column=1,
                                 tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

    def test_invalid_tile_row_value_larger_than_matrix_height(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tile(tile_zoom=1,
                                 tile_row=2,
                                 tile_column=0,
                                 tile_data=TestGeoPackageWriter.get_raster_data("jpeg"))

    def test_adding_mixed_raster_vector_tiles(self, get_gpkg_file_path):
        tiles_table_name = "Pirate_peg_leg"
        srs_id = 3857
        earth_radius_meters = 6378137

        srs_bounds = BoundingBox(min_x=-math.pi * earth_radius_meters,
                                 min_y=-math.pi * earth_radius_meters,
                                 max_x=math.pi * earth_radius_meters,
                                 max_y=math.pi * earth_radius_meters)

        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=join(get_gpkg_file_path),
                                            tile_table_name=tiles_table_name,
                                            srs_id=srs_id,
                                            srs_bounds=srs_bounds)

        red_tile_data = TestGeoPackageWriter.get_raster_data("png")
        blue_tile_data = TestGeoPackageWriter.get_raster_data("jpeg", "aliceblue")
        red_tile_row_expected = 2
        red_tile_column_expected = 3
        red_tile_zoom_expected = 6

        blue_tile_row_expected = 3
        blue_tile_column_expected = 4
        blue_tile_zoom_expected = 5
        gpkg_writer.add_tile(tile_row=red_tile_row_expected,
                             tile_column=red_tile_column_expected,
                             tile_zoom=red_tile_zoom_expected,
                             tile_data=red_tile_data)

        gpkg_writer.add_tile(tile_row=blue_tile_row_expected,
                             tile_column=blue_tile_column_expected,
                             tile_zoom=blue_tile_zoom_expected,
                             tile_data=blue_tile_data)

        TestGeoPackageWriter.assert_all_raster_tiles_tables(gpkg_file_path=gpkg_writer.file_path,
                                                            tiles_table_name=tiles_table_name)

        # assert the tile was added properly
        with get_database_connection(gpkg_writer.file_path) as db_conn:
            red_tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                              table_name=tiles_table_name,
                                                              tile_row=red_tile_row_expected,
                                                              tile_column=red_tile_column_expected,
                                                              zoom_level=red_tile_zoom_expected)
            assert red_tile_returned == Binary(red_tile_data)

            blue_tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                               table_name=tiles_table_name,
                                                               tile_row=blue_tile_row_expected,
                                                               tile_column=blue_tile_column_expected,
                                                               zoom_level=blue_tile_zoom_expected)
            assert blue_tile_returned == Binary(blue_tile_data)

            # assert the tile matrix entry was added
            tile_matrix_returned_red = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                      tile_table_name=tiles_table_name,
                                                                                      zoom_level=red_tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned_red) == 1
            assert tile_matrix_returned_red[0].table_name == tiles_table_name and \
                   tile_matrix_returned_red[0].matrix_height == 2 ** red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].matrix_width == 2 ** red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].zoom_level == red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].pixel_x_size == 2445.98490512564 and \
                   tile_matrix_returned_red[0].pixel_y_size == 2445.98490512564 and \
                   tile_matrix_returned_red[0].tile_height == 256 and \
                   tile_matrix_returned_red[0].tile_width == 256

            # assert the tile matrix entry was added
            tile_matrix_returned_blue = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                       tile_table_name=tiles_table_name,
                                                                                       zoom_level=blue_tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned_blue) == 1
            assert tile_matrix_returned_blue[0].table_name == tiles_table_name and \
                   tile_matrix_returned_blue[0].matrix_height == 2 ** blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].matrix_width == 2 ** blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].zoom_level == blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].pixel_x_size == 4891.96981025128 and \
                   tile_matrix_returned_blue[0].pixel_y_size == 4891.96981025128 and \
                   tile_matrix_returned_blue[0].tile_height == 256 and \
                   tile_matrix_returned_blue[0].tile_width == 256

            # assert the tile matrix set entry was added
            tile_matrix_set_returned = GeoPackageTiles.get_tile_matrix_set_entry_by_table_name(cursor=db_conn.cursor(),
                                                                                               table_name=tiles_table_name)
            assert tile_matrix_set_returned.srs_id == srs_id and \
                   tile_matrix_set_returned.min_x == srs_bounds.min_x and \
                   tile_matrix_set_returned.min_y == srs_bounds.min_y and \
                   tile_matrix_set_returned.max_x == srs_bounds.max_x and \
                   tile_matrix_set_returned.max_y == srs_bounds.max_y and \
                   tile_matrix_set_returned.table_name == tiles_table_name

            # assert the vector tiles table is in the gpkg contents table
            content = GeoPackageCore.get_content_entry_by_table_name(cursor=db_conn.cursor(),
                                                                     table_name=tiles_table_name)
            assert content.table_name == tiles_table_name and \
                   content.srs_id == srs_id and \
                   content.min_x == srs_bounds.min_x and \
                   content.min_y == srs_bounds.min_y and \
                   content.max_x == srs_bounds.max_x and \
                   content.max_y == srs_bounds.max_y and \
                   content.data_type == "tiles"

    def test_adding_tiles_bulk(self, get_gpkg_file_path):
        tiles_table_name = "Pirate_peg_leg"
        srs_id = 3857
        earth_radius_meters = 6378137

        srs_bounds = BoundingBox(min_x=-math.pi * earth_radius_meters,
                                 min_y=-math.pi * earth_radius_meters,
                                 max_x=math.pi * earth_radius_meters,
                                 max_y=math.pi * earth_radius_meters)

        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=join(get_gpkg_file_path),
                                            tile_table_name=tiles_table_name,
                                            srs_id=srs_id,
                                            srs_bounds=srs_bounds)

        red_tile_data = TestGeoPackageWriter.get_raster_data("png")
        blue_tile_data = TestGeoPackageWriter.get_raster_data("jpeg", "aliceblue")
        red_tile_row_expected = 2
        red_tile_column_expected = 3
        red_tile_zoom_expected = 6

        blue_tile_row_expected = 3
        blue_tile_column_expected = 4
        blue_tile_zoom_expected = 5

        red_tile_information = TileDataInformation(tile_data=red_tile_data,
                                                   tile_zoom=red_tile_zoom_expected,
                                                   tile_column=red_tile_column_expected,
                                                   tile_row=red_tile_row_expected)

        blue_tile_information = TileDataInformation(tile_data=blue_tile_data,
                                                    tile_zoom=blue_tile_zoom_expected,
                                                    tile_column=blue_tile_column_expected,
                                                    tile_row=blue_tile_row_expected)
        gpkg_writer.add_tiles(tiles=[red_tile_information, blue_tile_information])

        TestGeoPackageWriter.assert_all_raster_tiles_tables(gpkg_file_path=gpkg_writer.file_path,
                                                            tiles_table_name=tiles_table_name)

        # assert the tile was added properly
        with get_database_connection(gpkg_writer.file_path) as db_conn:
            red_tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                              table_name=tiles_table_name,
                                                              tile_row=red_tile_row_expected,
                                                              tile_column=red_tile_column_expected,
                                                              zoom_level=red_tile_zoom_expected)
            assert red_tile_returned == Binary(red_tile_data)

            blue_tile_returned = GeoPackageTiles.get_tile_data(cursor=db_conn.cursor(),
                                                               table_name=tiles_table_name,
                                                               tile_row=blue_tile_row_expected,
                                                               tile_column=blue_tile_column_expected,
                                                               zoom_level=blue_tile_zoom_expected)
            assert blue_tile_returned == Binary(blue_tile_data)

            # assert the tile matrix entry was added
            tile_matrix_returned_red = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                      tile_table_name=tiles_table_name,
                                                                                      zoom_level=red_tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned_red) == 1
            assert tile_matrix_returned_red[0].table_name == tiles_table_name and \
                   tile_matrix_returned_red[0].matrix_height == 2 ** red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].matrix_width == 2 ** red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].zoom_level == red_tile_zoom_expected and \
                   tile_matrix_returned_red[0].pixel_x_size == 2445.98490512564 and \
                   tile_matrix_returned_red[0].pixel_y_size == 2445.98490512564 and \
                   tile_matrix_returned_red[0].tile_height == 256 and \
                   tile_matrix_returned_red[0].tile_width == 256

            # assert the tile matrix entry was added
            tile_matrix_returned_blue = GeoPackageTiles.get_tile_matrix_for_zoom_level(cursor=db_conn.cursor(),
                                                                                       tile_table_name=tiles_table_name,
                                                                                       zoom_level=blue_tile_zoom_expected)
            # check to make sure only one
            assert len(tile_matrix_returned_blue) == 1
            assert tile_matrix_returned_blue[0].table_name == tiles_table_name and \
                   tile_matrix_returned_blue[0].matrix_height == 2 ** blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].matrix_width == 2 ** blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].zoom_level == blue_tile_zoom_expected and \
                   tile_matrix_returned_blue[0].pixel_x_size == 4891.96981025128 and \
                   tile_matrix_returned_blue[0].pixel_y_size == 4891.96981025128 and \
                   tile_matrix_returned_blue[0].tile_height == 256 and \
                   tile_matrix_returned_blue[0].tile_width == 256

            # assert the tile matrix set entry was added
            tile_matrix_set_returned = GeoPackageTiles.get_tile_matrix_set_entry_by_table_name(cursor=db_conn.cursor(),
                                                                                               table_name=tiles_table_name)
            assert tile_matrix_set_returned.srs_id == srs_id and \
                   tile_matrix_set_returned.min_x == srs_bounds.min_x and \
                   tile_matrix_set_returned.min_y == srs_bounds.min_y and \
                   tile_matrix_set_returned.max_x == srs_bounds.max_x and \
                   tile_matrix_set_returned.max_y == srs_bounds.max_y and \
                   tile_matrix_set_returned.table_name == tiles_table_name

            # assert the vector tiles table is in the gpkg contents table
            content = GeoPackageCore.get_content_entry_by_table_name(cursor=db_conn.cursor(),
                                                                     table_name=tiles_table_name)
            assert content.table_name == tiles_table_name and \
                   content.srs_id == srs_id and \
                   content.min_x == srs_bounds.min_x and \
                   content.min_y == srs_bounds.min_y and \
                   content.max_x == srs_bounds.max_x and \
                   content.max_y == srs_bounds.max_y and \
                   content.data_type == "tiles"

    def test_adding_tiles_bulk_invalid_tiles_empty(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tiles(tiles=[])

    def test_adding_tiles_bulk_invalid_tiles_none(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tiles(tiles=None)

    def test_adding_tiles_bulk_invalid_tiles_types_mixed(self, get_gpkg_file_path):
        gpkg_writer = GeoPackageTilesWriter(gpkg_file_path=get_gpkg_file_path,
                                            tile_table_name="table",
                                            srs_id=9804,
                                            srs_bounds=BoundingBox(1.0, 2.0, 3.0, 4.0))

        with raises(ValueError):
            gpkg_writer.add_tiles(tiles=[TileDataInformation(tile_row=1,
                                                             tile_column=1,
                                                             tile_zoom=1,
                                                             tile_data=self.get_raster_data("jpeg")),
                                         TileDataInformation(tile_row=0,
                                                             tile_column=0,
                                                             tile_zoom=2,
                                                             tile_data=TestGeoPackageVectorTiles.get_mapbox_vector_tile_data())])

    @pytest.fixture(scope="function")
    def get_gpkg_file_path(self):
        gpkg_file_path = join(gettempdir(), uuid4().hex + '.gpkg')
        yield gpkg_file_path
        remove(gpkg_file_path)

    @staticmethod
    def get_raster_data(image_type, color="red"):
        img = new("RGB", (256, 256), color)
        return img_to_buf(img, image_type).read()

    @staticmethod
    def assert_default_tiles_tables(gpkg_file_path, tiles_table_name):
        """
        Checks to make sure all the tiles tables are accounted for: gpkg_tile_matrix_set, gpkg_tile_matrix,
        <tile_pyramid_user_data_table>
        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str
        :param tiles_table_name: the name of the tiles table
        :type tiles_table_name: str
        """
        with get_database_connection(gpkg_file_path) as db_conn:
            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_TILE_MATRIX_TABLE_NAME)

            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_TILE_MATRIX_SET_TABLE_NAME)

            assert table_exists(cursor=db_conn.cursor(),
                                table_name=tiles_table_name)

    @staticmethod
    def assert_default_core_tables(gpkg_file_path):
        """
        Checks to make sure all the core tables are accounted for: gpkg_contents, gpkg_spatial_ref_sys

        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str
        """
        with get_database_connection(gpkg_file_path) as db_conn:
            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_CONTENTS_TABLE_NAME)

            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_SPATIAL_REFERENCE_SYSTEM_TABLE_NAME)

    @staticmethod
    def assert_default_vector_tiles_tables(gpkg_file_path):
        """
        Checks to make sure all the vector tables are accounted for: gpkgext_vt_layers, gpkgext_vt_fields

        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str
        """
        with get_database_connection(gpkg_file_path) as db_conn:
            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_VECTOR_LAYERS_TABLE_NAME)

            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_VECTOR_FIELDS_TABLE_NAME)

            assert table_exists(cursor=db_conn.cursor(),
                                table_name=GEOPACKAGE_EXTENSIONS_TABLE_NAME)

    @staticmethod
    def assert_vector_tiles_extensions_registered(gpkg_file_path,
                                                  tiles_table_extension):
        """
        Checks to make sure all the vector extensions are accounted for: gpkgext_vt_layers, gpkgext_vt_fields,
        and the vector tiles table with the different encoding

        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str

        :param tiles_table_extension: MapBoxVectorTilesExtension object or GeoJSONVectorTilesExtension object
        :type tiles_table_extension: Extension
        """
        with get_database_connection(gpkg_file_path) as db_conn:
            assert GeoPackageExtensions.has_extension(cursor=db_conn.cursor(),
                                                      extension=GeoPackageVectorLayers())

            assert GeoPackageExtensions.has_extension(cursor=db_conn.cursor(),
                                                      extension=GeoPackageVectorFields())

            assert GeoPackageExtensions.has_extension(cursor=db_conn.cursor(),
                                                      extension=tiles_table_extension)

    @staticmethod
    def assert_all_vector_tiles_tables(gpkg_file_path,
                                       tiles_table_extension):
        """
        Checks all the basic tables are existent for vector tiles and if the extensions have been registered properly

        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str

        :param tiles_table_extension: MapBoxVectorTilesExtension object or GeoJSONVectorTilesExtension object
        :type tiles_table_extension: Extension
        """

        TestGeoPackageWriter.assert_default_core_tables(gpkg_file_path=gpkg_file_path)
        TestGeoPackageWriter.assert_default_tiles_tables(gpkg_file_path=gpkg_file_path,
                                                         tiles_table_name=tiles_table_extension.table_name)
        TestGeoPackageWriter.assert_default_vector_tiles_tables(gpkg_file_path=gpkg_file_path)
        TestGeoPackageWriter.assert_vector_tiles_extensions_registered(gpkg_file_path=gpkg_file_path,
                                                                       tiles_table_extension=
                                                                       GeoPackageMapBoxVectorTiles(
                                                                           vector_tiles_table_name
                                                                           =tiles_table_extension.table_name))

    @staticmethod
    def assert_all_raster_tiles_tables(gpkg_file_path,
                                       tiles_table_name):
        """
        Checks all the basic tables are existent for raster tiles

        :param gpkg_file_path: path to the gpkg to check
        :type gpkg_file_path: str

        :param tiles_table_name: the name of the tiles table
        :type tiles_table_name: str
        """

        TestGeoPackageWriter.assert_default_core_tables(gpkg_file_path=gpkg_file_path)
        TestGeoPackageWriter.assert_default_tiles_tables(gpkg_file_path=gpkg_file_path,
                                                         tiles_table_name=tiles_table_name)
