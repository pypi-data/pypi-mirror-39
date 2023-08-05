"""Use a directory of zoom/row/column tiles as input."""

from itertools import chain
import logging
import numpy as np
import numpy.ma as ma
import os
from shapely.geometry import box

from mapchete.config import validate_values
from mapchete.errors import MapcheteConfigError
from mapchete.formats import base, load_output_writer
from mapchete.io import path_exists, absolute_path, read_json
from mapchete.io.vector import reproject_geometry, read_vector_window
from mapchete.io.raster import read_raster_window, create_mosaic, resample_from_array
from mapchete.tile import BufferedTilePyramid


logger = logging.getLogger(__name__)
METADATA = {
    "driver_name": "TileDirectory",
    "data_type": None,
    "mode": "r",
    "file_extensions": None
}


class InputData(base.InputData):
    """
    Main input class.

    Parameters
    ----------
    input_params : dictionary
        driver specific parameters

    Attributes
    ----------
    path : string
        path to Mapchete file
    pixelbuffer : integer
        buffer around output tiles
    pyramid : ``tilematrix.TilePyramid``
        output ``TilePyramid``
    crs : ``rasterio.crs.CRS``
        object describing the process coordinate reference system
    srid : string
        spatial reference ID of CRS (e.g. "{'init': 'epsg:4326'}")
    """

    METADATA = METADATA

    def __init__(self, input_params, **kwargs):
        """Initialize."""
        super(InputData, self).__init__(input_params, **kwargs)

        if "abstract" in input_params:
            self._params = input_params["abstract"]
            self.path = absolute_path(
                path=self._params["path"],
                base_dir=input_params["conf_dir"]
            )
            # define pyramid
            self.td_pyramid = BufferedTilePyramid(
                self._params["type"],
                metatiling=self._params.get("metatiling", 1),
                tile_size=self._params.get("tile_size", 256),
                pixelbuffer=self._params.get("pixelbuffer", 0)
            )

        elif "path" in input_params:
            self.path = absolute_path(
                path=input_params["path"], base_dir=input_params.get("conf_dir")
            )
            try:
                params = read_json(os.path.join(self.path, "metadata.json"))
            except FileNotFoundError:
                raise MapcheteConfigError(
                    "Cannot find metadata.json in %s" % input_params["path"]
                )
            # define pyramid
            self.td_pyramid = BufferedTilePyramid(
                params["pyramid"]["grid"]["type"],
                metatiling=params["pyramid"].get("metatiling", 1),
                tile_size=params["pyramid"].get("tile_size", 256),
                pixelbuffer=params["pyramid"].get("pixelbuffer", 0)
            )

            output = load_output_writer(
                dict(
                    params["driver"],
                    metatiling=self.td_pyramid.metatiling,
                    pixelbuffer=self.td_pyramid.pixelbuffer,
                    pyramid=self.td_pyramid,
                    type=self.td_pyramid.type,
                    path=self.path
                ),
                readonly=True
            )
            logger.debug(output)
            self._params = dict(
                path=self.path,
                type=params["pyramid"]["grid"]["type"],
                metatiling=params["pyramid"].get("metatiling", 1),
                pixelbuffer=params["pyramid"].get("pixelbuffer", 0),
                tile_size=params["pyramid"].get("tile_size", 256),
                extension=output.file_extension.split(".")[-1],
                **params["driver"]
            )

        # validate parameters
        validate_values(
            self._params,
            [
                ("path", str),
                ("type", str),
                ("extension", str)
            ]
        )
        if not self._params["extension"] in [
            "tif", "vrt", "png", "jpg", "mixed", "jp2", "geojson"
        ]:
            raise MapcheteConfigError(
                "invalid file extension given: %s" % self._params["extension"]
            )
        self._ext = self._params["extension"]

        # additional params
        self._bounds = self._params.get("bounds", self.td_pyramid.bounds)
        self._file_type = (
            "vector" if self._params["extension"] == "geojson" else "raster"
        )
        if self._file_type == "raster":
            self._params["count"] = self._params.get(
                "count", self._params.get("bands", None)
            )
            validate_values(self._params, [("dtype", str), ("count", int)])
            self._profile = {
                "nodata": self._params.get("nodata", 0),
                "dtype": self._params["dtype"],
                "count": self._params["count"]
            }
        else:
            self._profile = None

    def open(self, tile, **kwargs):
        """
        Return InputTile object.

        Parameters
        ----------
        tile : ``Tile``

        Returns
        -------
        input tile : ``InputTile``
            tile view of input data
        """
        return InputTile(
            tile,
            tiles_paths=[
                (_tile, _path)
                for _tile, _path in [
                    (t, os.path.join(*([
                        self.path, str(t.zoom), str(t.row), str(t.col)
                        ])) + "." + self._ext)
                    for t in self.td_pyramid.tiles_from_bounds(
                        tile.bounds, tile.zoom)
                ]
                if path_exists(_path)
            ],
            file_type=self._file_type,
            profile=self._profile,
            **kwargs
        )

    def bbox(self, out_crs=None):
        """
        Return data bounding box.

        Parameters
        ----------
        out_crs : ``rasterio.crs.CRS``
            rasterio CRS object (default: CRS of process pyramid)

        Returns
        -------
        bounding box : geometry
            Shapely geometry object
        """
        return reproject_geometry(
            box(*self._bounds),
            src_crs=self.td_pyramid.crs,
            dst_crs=self.pyramid.crs if out_crs is None else out_crs
        )


class InputTile(base.InputTile):
    """
    Target Tile representation of input data.

    Parameters
    ----------
    tile : ``Tile``
    kwargs : keyword arguments
        driver specific parameters

    Attributes
    ----------
    tile : tile : ``Tile``
    """

    def __init__(self, tile, **kwargs):
        """Initialize."""
        self.tile = tile
        self._tiles_paths = kwargs["tiles_paths"]
        self._file_type = kwargs["file_type"]
        self._profile = kwargs["profile"]

    def read(
        self, validity_check=False, indexes=None, resampling="nearest",
        dst_nodata=None, gdal_opts=None
    ):
        """
        Read reprojected & resampled input data.

        Parameters
        ----------
        validity_check : bool
            vector file: also run checks if reprojected geometry is valid,
            otherwise throw RuntimeError (default: True)

        indexes : list or int
            raster file: a list of band numbers; None will read all.
        resampling : string
            raster file: one of "nearest", "average", "bilinear" or "lanczos"
        dst_nodata : int or float, optional
            raster file: if not set, the nodata value from the source dataset
            will be used
        gdal_opts : dict
            raster file: GDAL options passed on to rasterio.Env()

        Returns
        -------
        data : list for vector files or numpy array for raster files
        """
        if self._file_type == "vector":
            if self.is_empty():
                return []
            return list(chain.from_iterable([
                read_vector_window(
                    _path, self.tile, validity_check=validity_check)
                for _, _path in self._tiles_paths
            ]))
        else:
            if self.is_empty():
                count = (len(indexes) if indexes else self._profile["count"], )
                return ma.masked_array(
                    data=np.full(
                        count + self.tile.shape, self._profile["nodata"],
                        dtype=self._profile["dtype"]),
                    mask=True
                )
            tiles = [
                (
                    _tile,
                    read_raster_window(
                        _path, _tile, indexes=indexes, resampling=resampling,
                        src_nodata=self._profile["nodata"], dst_nodata=dst_nodata,
                        gdal_opts=gdal_opts
                    )
                )
                for _tile, _path in self._tiles_paths
            ]
            return resample_from_array(
                in_raster=create_mosaic(tiles=tiles, nodata=self._profile["nodata"]),
                out_tile=self.tile,
                resampling=resampling,
                nodataval=self._profile["nodata"]
            )

    def is_empty(self):
        """
        Check if there is data within this tile.

        Returns
        -------
        is empty : bool
        """
        return len(self._tiles_paths) == 0
