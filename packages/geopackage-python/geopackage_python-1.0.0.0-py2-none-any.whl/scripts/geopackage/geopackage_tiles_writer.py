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
import imghdr
import json
from contextlib import contextmanager

from scripts.geopackage.extensions.vector_tiles.vector_tiles_content_entry import VectorTilesContentEntry

try:
    from cStringIO import StringIO as ioBuffer
except ImportError:
    from io import BytesIO as ioBuffer
from os import path

import mapbox_vector_tile
from enum import Enum

from scripts.common.bounding_box import BoundingBox
from scripts.common.tile_scheme import TileScheme
from scripts.common.zoom_times_two import ZoomTimesTwo
from scripts.geopackage.core.geopackage_core import GeoPackageCore
from scripts.geopackage.core.spatial_ref_system_entry import SpatialReferenceSystemEntry
from scripts.geopackage.extensions.vector_tiles.geopackage_geojson_vector_tiles import GeoPackageGeoJSONVectorTiles
from scripts.geopackage.extensions.vector_tiles.geopackage_mapbox_vector_tiles import GeoPackageMapBoxVectorTiles
from scripts.geopackage.srs.ellipsoidal_mercator import EllipsoidalMercator
from scripts.geopackage.srs.geodetic_nsg import GeodeticNSG
from scripts.geopackage.srs.mercator import Mercator
from scripts.geopackage.srs.scaled_world_mercator import ScaledWorldMercator
from scripts.geopackage.srs.undefined_cartesian_coord_ref_sys import UndefinedCartesianCoordinateReferenceSystem
from scripts.geopackage.srs.undefined_geographic_coord_ref_sys import UndefinedGeographicCoordinateReferenceSystem
from scripts.geopackage.tiles.geopackage_tiles import GeoPackageTiles
from scripts.geopackage.tiles.tile_matrix_entry import TileMatrixEntry
from scripts.geopackage.tiles.tiles_content_entry import TilesContentEntry
from scripts.geopackage.tiles.tile_data_information import TileDataInformation
from scripts.geopackage.utility.sql_utility import get_database_connection, table_exists
from sqlite3 import Binary


class TileType(Enum):
    """
    Tile encoding types that are supported in the GeoPackageTileWriter
    """
    PNG = "png",
    JPEG = "jpeg",
    MAPBOX = "mapbox",
    GEOJSON = "geojson"

    def is_raster_type(self):
        """
        Returns true if the tile type is of type raster. Which is either PNG or JPEG

        :return: True if the tile type is of type PNG or JPEG, false otherwise
        :rtype: bool
        """
        return self == TileType.PNG or self == TileType.JPEG

    def is_vector_tile_type(self):
        """
        Returns true if the tile type is of type vector-tiles. Which is either MapBox or GeoJSON

        :return: True if the tile type is of type MapBox or GeoJSON, false otherwise
        :rtype: bool
        """
        return self == TileType.MAPBOX or self == TileType.GEOJSON


class GeoPackageTilesWriter(object):
    """
    Writes raster or vector-tiles to a GeoPackage. Each instance will write to a single GeoPackage tiles table.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__database_connection.close()

    def __init__(self,
                 gpkg_file_path,
                 tile_table_name,
                 srs_id,
                 srs_bounds,
                 tile_size=(256, 256),
                 tile_scheme=ZoomTimesTwo(base_matrix_width=1, base_matrix_height=1),
                 tile_data_bounding_box=None,
                 identifier=""):
        """
        Constructor

        :param gpkg_file_path: the path where the GeoPackage should be written to or an existing GeoPackage to write
        to
        :type gpkg_file_path: str

        :param tile_table_name:  The name of the tiles table to write to
        :type tile_table_name: str

        :param srs_id: the Spatial Reference System identifier (i.e. 4326, 3857)
        :type srs_id: int

        :param tile_size:  The size of the tiles in the form of a tuple (i.e. (256,256), (512,256) ) where the first
        value is the width and the second value is the height
        :type tile_size: ``int(width), int(height)``

        :param srs_bounds: The full bounds of the Spatial Reference System
        (i.e. for EPSG:4326 the bounds would be (min_x=-180.0,min_y=-90.0,max_x=180.0,max_y=90.0)
        :type srs_bounds: BoundingBox

        :param tile_data_bounding_box: (optional) The bounds of the tile data only.  If not specified the full bounds of the
        Spatial Reference System will be used.
        :type tile_data_bounding_box:BoundingBox

        :param tile_scheme: (optional) The tiling scheme of the data. Defines the dimensions or the grid by zoom level
        (i.e. zoom level 0 have 1 tile, zoom level 1 have 2 by 2 or 4 tiles, zoom level 2 have 4 by 4 or 16 tiles etc..)
        :type tile_scheme: TileScheme

        :param identifier: (optional) Human readable identifier to describe the tile set
        :type identifier: str
        """
        # check the gpkg path
        if path.isdir(gpkg_file_path):
            raise ValueError("The gpkg_file_path cannot be a path to a directory. Path given: {path}"
                             .format(path=gpkg_file_path))
        self.file_path = gpkg_file_path

        # create the file if it doesn't exist
        if not path.exists(gpkg_file_path):
            with open(gpkg_file_path, 'w'):
                pass

        # save the variables
        self.__database_connection = get_database_connection(file_path=gpkg_file_path)
        self.tile_table_name = tile_table_name
        self.srs_bounds = srs_bounds
        self.data_bounds = tile_data_bounding_box if tile_data_bounding_box is not None else srs_bounds
        self.identifier = identifier
        self.tile_size = tile_size
        self.tile_scheme = tile_scheme
        self.tile_type = None

        # create default tables if they do not exist
        GeoPackageCore.create_core_tables(cursor=self.__database_connection.cursor())

        # set the spatial reference system variable
        if srs_id == EllipsoidalMercator.srs_identifier:
            self.spatial_reference_system = EllipsoidalMercator()
        elif srs_id == GeodeticNSG.srs_identifier:
            self.spatial_reference_system = GeodeticNSG()
        elif srs_id == Mercator.srs_identifier:
            self.spatial_reference_system = Mercator()
        elif srs_id == ScaledWorldMercator.srs_identifier:
            self.spatial_reference_system = ScaledWorldMercator()
        elif srs_id == UndefinedCartesianCoordinateReferenceSystem.srs_identifier:
            self.spatial_reference_system = UndefinedCartesianCoordinateReferenceSystem()
        elif srs_id == UndefinedGeographicCoordinateReferenceSystem.srs_identifier:
            self.spatial_reference_system = UndefinedGeographicCoordinateReferenceSystem()
        else:
            self.spatial_reference_system = SpatialReferenceSystemEntry(srs_name="EPSG:{0}".format(srs_id),
                                                                        srs_id=srs_id,
                                                                        organization_coordsys_id=srs_id,
                                                                        definition="",
                                                                        description="Added via GeoPackage-Python",
                                                                        organization="EPSG")
        # add the spatial reference system to the GeoPackage
        GeoPackageCore.insert_spatial_reference_system_row(cursor=self.__database_connection.cursor(),
                                                           spatial_reference_system=self.spatial_reference_system)
        # commit changes to the GeoPackage
        self.__database_connection.commit()

    def add_tiles(self,
                  tiles):

        """
        Adds the tiles to the GeoPackage

        :param tiles: the list of tiles to add to the GeoPackage
        :return: list of TileDataInformation
        """
        if tiles is None or len(tiles) == 0:
            raise ValueError("The list of tiles cannot be empty or None.")

        # check valid tile types: no mixing of vector and raster, AND no mixing of the two different vector tiles
        for index, tile in enumerate(tiles):
            for second_index, second_tile in enumerate(tiles, start=index + 1):
                tile_type1 = self.get_tile_type_from_data(tile_data=tile.tile_data)
                tile_type2 = self.get_tile_type_from_data(tile_data=second_tile.tile_data)
                are_compatible, message = self.__are_tile_types_compatible(tile_type1=tile_type1,
                                                                           tile_type2=tile_type2)
                if not are_compatible:
                    raise ValueError(message)
        # since all the tile types compatible, just grab the first one
        tile_type = self.get_tile_type_from_data(tiles[0].tile_data)

        # set the previous tile_type set
        if self.tile_type is None:
            self.tile_type = tile_type
        else:
            # check if this type is compatible with previous type
            is_compatible, message = self.__are_tile_types_compatible(tile_type, self.tile_type)
            if not is_compatible:
                raise ValueError(message)

        gpkg_tiles_creator = self.__get_tiles_creator_by_tile_type(tile_type=tile_type)

        self.__add_default_tables(gpkg_tiles_creator=gpkg_tiles_creator,
                                  tile_table_name=self.tile_table_name,
                                  tile_type=tile_type)

        # add matrix entries
        for tile in tiles:
            matrix_entry = self.__add_tile_matrix_entry_for_zoom_level(gpkg_tiles_creator=gpkg_tiles_creator,
                                                                       tile_zoom=tile.zoom_level)

            self.__check_valid_range_tile_row_tle_column_for_matrix_entry(matrix_entry=matrix_entry,
                                                                          tile_row=tile.tile_row,
                                                                          tile_column=tile.tile_column)
        # add the tile data
        gpkg_tiles_creator.insert_or_update_tile_data_bulk(cursor=self.__database_connection.cursor(),
                                                           table_name=self.tile_table_name,
                                                           tiles=[TileDataInformation(tile_row=tile.tile_row,
                                                                                      tile_column=tile.tile_column,
                                                                                      tile_zoom=tile.zoom_level,
                                                                                      tile_data=Binary(tile.tile_data))
                                                                  for tile in tiles])

        self.__database_connection.commit()

    def __get_tiles_creator_by_tile_type(self,
                                         tile_type):
        """
        Gets the gpkg tiles creator associated with the encoding specified

        :param tile_type: the tile type encoding
        :type tile_type: TileType

        :return: the gpkg tiles creator associated with the encoding specified
        :rtype: GeoPackageTiles
        """

        if tile_type == TileType.JPEG or tile_type == TileType.PNG:
            # raster tiles
            gpkg_tiles_creator = GeoPackageTiles()

        elif tile_type == TileType.MAPBOX:
            # map box vector tiles
            gpkg_tiles_creator = GeoPackageMapBoxVectorTiles(vector_tiles_table_name=self.tile_table_name)

        elif tile_type == TileType.GEOJSON:
            # geojson vector tiles
            gpkg_tiles_creator = GeoPackageGeoJSONVectorTiles(vector_tiles_table_name=self.tile_table_name)

        else:
            raise ValueError("Unsupported Tile type {type}. Unable to add tile data".format(type=tile_type))

        return gpkg_tiles_creator

    def add_tile(self,
                 tile_row,
                 tile_column,
                 tile_zoom,
                 tile_data):
        """
        Adds the tile to the GeoPackage.  The tile coordinates must be of Tile Origin upper left.

        :param tile_row: the y coordinate of the tile. 0 to tile_matrix matrix_height - 1
        :type tile_row: int

        :param tile_column: the x coordinate of the tile.  0 to tile_matrix matrix_width - 1
        :type tile_column: int

        :param tile_zoom: the zoom level of the tile (z coordinate)
        :type tile_zoom: int

        :param tile_data: the tile data encoded in JPEG, PNG, MapBox Vector Tile (.pbf), or GeoJSON
        :type tile_data: Binary
        """
        self.add_tiles(tiles=[TileDataInformation(tile_row=tile_row,
                                                  tile_column=tile_column,
                                                  tile_zoom=tile_zoom,
                                                  tile_data=tile_data)])

    @staticmethod
    def __are_tile_types_compatible(tile_type1, tile_type2):
        """
        Returns true if the tiles types are compatible (the same or able to be mixed together) with a blank message,
        false otherwise with a message what is incorrect

        :param tile_type1: the first tile type to compare to
        :type tile_type1: TileType

        :param tile_type2: the second tile type to compare
        :type tile_type2: TileType

        :return: Returns true if the tiles types are compatible (the same or able to be mixed together) with a blank
        message, false otherwise with a message what is incorrect
        :rtype: tuple(bool, str)
        """
        # check to see if there is a mix of raster and vector types, not allowed!
        if (tile_type1.is_raster_type() and tile_type2.is_vector_tile_type()) or \
                (tile_type1.is_vector_tile_type() and tile_type2.is_raster_type()):
            return False, "Cannot mix writing vector-tiles and raster tiles with the same GeoPackage Writer."

        # check to make sure if it is a vector type, it is the same
        if tile_type1.is_vector_tile_type() and tile_type2.is_vector_tile_type():
            if tile_type1 != tile_type2:
                return False, "Cannot mix two different types of vector-tile data encodings. Must all be GeoJSON " \
                              "vector tiles or MapBox vector tiles."
        return True, ""

    @staticmethod
    def get_tile_type_from_data(tile_data):
        """
        Determines the tile type based on the encoded data. Throws a ValueError if unable to determine the type.

        :param tile_data: the tile data to determine the encoding of
        :type tile_data: Binary

        :rtype: TileType
        """
        string_tile_data = ioBuffer(tile_data).read()

        # check to see if it is raster data
        mime_type = imghdr.what(file=None, h=string_tile_data)

        if mime_type is 'png':
            return TileType.PNG
        elif mime_type is 'jpeg':
            return TileType.JPEG
        elif mime_type is not None:
            raise ValueError("Unsupported encoded data type: {type}".format(type=mime_type))

        # check to see if it is mapbox vector tile data
        try:
            if len(mapbox_vector_tile.decode(tile_data)) != 0:
                return TileType.MAPBOX
        except:
            pass

        # check to see if it is GeoJSON data
        try:
            json.loads(string_tile_data)
            return TileType.GEOJSON
        except ValueError:
            pass
        raise ValueError("Unsupported tile_data. Is not one of the following {types}"
                         .format(types=", ".join([tile_type.value[0]
                                                  for tile_type
                                                  in TileType])))

    @staticmethod
    def calc_resolutions(bounding_box,
                         tile_size,
                         zoom_level,
                         tile_scheme):
        """
        Returns the pixel_x_size, pixel_y_size given the following values.

        :param tile_scheme: Gives the dimensions of the tile grid given a zoom level
        :type tile_scheme: TileScheme

        :param bounding_box:  The bounds of the data in the CRS coordinates (meters, decimal degrees etc..)
        :type bounding_box: BoundingBox

        :ivar tile_size: the size of each tile in pixel
        :type tile_size: ``int(with), int(height)``

        :param zoom_level: the zoom level to calculate the resolution for
        :type zoom_level: int

        :return: tuple of pixel_x_size and pixel_y_size
        :rtype: tuple(float, float)
        """

        width = (bounding_box.max_x - bounding_box.min_x)
        height = (bounding_box.max_y - bounding_box.min_y)

        matrix_width, matrix_height = tile_scheme.get_matrix_dimensions(zoom_level=zoom_level)

        return ((width / tile_size[0]) / matrix_width), \
               ((height / tile_size[1]) / matrix_height)

    @staticmethod
    def __check_valid_range_tile_row_tle_column_for_matrix_entry(matrix_entry,
                                                                 tile_row,
                                                                 tile_column):
        """
        Checks to see if the tile_row and tile_column are in a valid range according to the tile matrix entry given.
        Will raise an exception if there is an invalid value.

        :param matrix_entry:
        :type matrix_entry: list of TileMatrixEntry

        :param tile_row: the y coordinate of the tile. 0 to tile_matrix matrix_height - 1
        :type tile_row: int

        :param tile_column: the x coordinate of the tile.  0 to tile_matrix matrix_width - 1
        :type tile_column: int
        """

        if tile_column < 0 or tile_column > matrix_entry[0].matrix_width - 1:
            raise ValueError("tile_column {tile_column} needs to be within the range of the matrix_width "
                             "[0, {width}]".format(tile_column=tile_column,
                                                   width=matrix_entry[0].matrix_width))
        elif tile_row < 0 or tile_row > matrix_entry[0].matrix_height - 1:
            raise ValueError("tile_row {tile_row} needs to be within the range of the matrix_height "
                             "[0, {height}]".format(tile_row=tile_row,
                                                    height=matrix_entry[0].matrix_height))

    def __add_tile_matrix_entry_for_zoom_level(self,
                                               gpkg_tiles_creator,
                                               tile_zoom):
        """
        Adds a tile matrix entry for the given zoom level.  If the matrix entry for the zoom level already exists, will
        not add another.

        :return: the gpkg tiles creator associated with the encoding specified
        :rtype: GeoPackageTiles

        :param tile_zoom: the zoom level the tile matrix entry should be added for
        :type tile_zoom: int
        :return: the tile matrix entry created or found
        :rtype: list of TileMatrixEntry
        """
        # add tile matrix
        self.__add_tile_matrix_entry(tile_zoom=tile_zoom,
                                     gpkg_tiles_creator=gpkg_tiles_creator)

        # check to make sure the tile_row and tile_column are within the matrix dimensions
        matrix_entry = gpkg_tiles_creator.get_tile_matrix_for_zoom_level(cursor=self.__database_connection.cursor(),
                                                                         zoom_level=tile_zoom,
                                                                         tile_table_name=self.tile_table_name)
        if len(matrix_entry) > 1 or len(matrix_entry) < 0:
            # problem there should only be 1 matrix
            raise ValueError("There are multiple entries in the gpkg_tile_matrix table for this zoom_level and tiles "
                             "table name. There should only be one per zoom per tiles table. Remove the entries that "
                             "are invalid and try to add to the tiles table again.")

        return matrix_entry

    def __add_default_tables(self,
                             gpkg_tiles_creator,
                             tile_table_name,
                             tile_type):
        """
        Adds the default tables needed to add the tile to the GeoPackage

        :param gpkg_tiles_creator: the tile creator for the correct tables
        :type gpkg_tiles_creator: GeoPackageTiles

        :param tile_table_name: the name of the tiles table
        :type tile_table_name: str

        :param tile_type: the type of tile encoding
        :type tile_type: TileType
        """
        # add the default tiles tables
        gpkg_tiles_creator.create_default_tiles_tables(cursor=self.__database_connection.cursor())

        # check to make sure the tile pyramid user data table exists
        if not table_exists(cursor=self.__database_connection.cursor(),
                            table_name=tile_table_name):
            self.__add_tile_pyramid_user_data_table(gpkg_tiles_creator=gpkg_tiles_creator,
                                                    tile_type=tile_type)

    def __add_tile_matrix_entry(self,
                                tile_zoom,
                                gpkg_tiles_creator):
        """
        Adds the Tile Matrix entry to the GeoPackage if one does not currently exist for the zoom level

        :param tile_zoom: the zoom level that needs a tile matrix entry
        :type tile_zoom: int

        :param gpkg_tiles_creator: the GeoPackageTiles creator
        :type gpkg_tiles_creator: GeoPackageTiles
        """
        if len(gpkg_tiles_creator.get_tile_matrix_for_zoom_level(cursor=self.__database_connection.cursor(),
                                                                 tile_table_name=self.tile_table_name,
                                                                 zoom_level=tile_zoom)) < 1:
            # add tile matrix
            matrix_width, matrix_height = self.tile_scheme.get_matrix_dimensions(zoom_level=tile_zoom)

            pixel_x_size, pixel_y_size = GeoPackageTilesWriter.calc_resolutions(bounding_box=self.srs_bounds,
                                                                                tile_size=self.tile_size,
                                                                                zoom_level=tile_zoom,
                                                                                tile_scheme=self.tile_scheme)

            gpkg_tiles_creator.insert_or_update_gpkg_tile_matrix_row(cursor=self.__database_connection.cursor(),
                                                                     tile_matrix_entry=TileMatrixEntry(
                                                                         table_name=self.tile_table_name,
                                                                         zoom_level=tile_zoom,
                                                                         matrix_height=matrix_height,
                                                                         matrix_width=matrix_width,
                                                                         tile_height=self.tile_size[1],
                                                                         tile_width=self.tile_size[0],
                                                                         pixel_x_size=pixel_x_size,
                                                                         pixel_y_size=pixel_y_size))

    def __add_tile_pyramid_user_data_table(self, gpkg_tiles_creator, tile_type):
        """
        Adds the pyramid user data table and includes the information in the gpkg_contents table as well as the
        gpkg_tile_matrix_set table

        :param gpkg_tiles_creator: the GeoPackage Tiles creator
        :type gpkg_tiles_creator: GeoPackageTiles

        :param tile_type:
        :type tile_type: TileType
        """
        tiles_content = TilesContentEntry(table_name=self.tile_table_name,
                                          identifier=self.identifier,
                                          min_x=self.data_bounds.min_x,
                                          min_y=self.data_bounds.min_y,
                                          max_x=self.data_bounds.max_x,
                                          max_y=self.data_bounds.max_y,
                                          srs_id=self.spatial_reference_system.srs_id) if tile_type.is_raster_type() \
            else VectorTilesContentEntry(table_name=self.tile_table_name,
                                         identifier=self.identifier,
                                         min_x=self.data_bounds.min_x,
                                         min_y=self.data_bounds.min_y,
                                         max_x=self.data_bounds.max_x,
                                         max_y=self.data_bounds.max_y,
                                         srs_id=self.spatial_reference_system.srs_id)

        gpkg_tiles_creator.create_pyramid_user_data_table(cursor=self.__database_connection.cursor(),
                                                          tiles_content=tiles_content)

        matrix_content = TilesContentEntry(table_name=self.tile_table_name,
                                           identifier=self.identifier,
                                           min_x=self.srs_bounds.min_x,
                                           min_y=self.srs_bounds.min_y,
                                           max_x=self.srs_bounds.max_x,
                                           max_y=self.srs_bounds.max_y,
                                           srs_id=self.spatial_reference_system.srs_id) if tile_type.is_raster_type() \
            else VectorTilesContentEntry(table_name=self.tile_table_name,
                                         identifier=self.identifier,
                                         min_x=self.srs_bounds.min_x,
                                         min_y=self.srs_bounds.min_y,
                                         max_x=self.srs_bounds.max_x,
                                         max_y=self.srs_bounds.max_y,
                                         srs_id=self.spatial_reference_system.srs_id)

        gpkg_tiles_creator.insert_or_update_gpkg_tile_matrix_set_row(cursor=self.__database_connection.cursor(),
                                                                     tiles_content=matrix_content,
                                                                     update_contents_table=False)
