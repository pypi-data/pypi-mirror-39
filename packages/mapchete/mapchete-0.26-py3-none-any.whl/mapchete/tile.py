"""Mapchtete handling tiles."""
from cached_property import cached_property
from shapely.geometry import box
from tilematrix import Tile, TilePyramid


class BufferedTilePyramid(TilePyramid):
    """
    A special tile pyramid with fixed pixelbuffer and metatiling.

    Parameters
    ----------
    pyramid_type : string
        pyramid projection type (``geodetic`` or ``mercator``)
    metatiling : integer
        metatile size (default: 1)
    pixelbuffer : integer
        buffer around tiles in pixel (default: 0)

    Attributes
    ----------
    tile_pyramid : ``TilePyramid``
        underlying ``TilePyramid``
    metatiling : integer
        metatile size
    pixelbuffer : integer
        tile buffer size in pixels
    """

    def __init__(
        self, pyramid_type, metatiling=1, tile_size=256, pixelbuffer=0
    ):
        """Initialize."""
        TilePyramid.__init__(
            self, pyramid_type, metatiling=metatiling, tile_size=tile_size)
        self.tile_pyramid = TilePyramid(
            pyramid_type, metatiling=metatiling, tile_size=tile_size)
        self.metatiling = metatiling
        if isinstance(pixelbuffer, int) and pixelbuffer >= 0:
            self.pixelbuffer = pixelbuffer
        else:
            raise ValueError("pixelbuffer has to be a non-negative int")

    def tile(self, zoom, row, col):
        """
        Return ``BufferedTile`` object of this ``BufferedTilePyramid``.

        Parameters
        ----------
        zoom : integer
            zoom level
        row : integer
            tile matrix row
        col : integer
            tile matrix column

        Returns
        -------
        buffered tile : ``BufferedTile``
        """
        tile = self.tile_pyramid.tile(zoom, row, col)
        return BufferedTile(tile, pixelbuffer=self.pixelbuffer)

    def tiles_from_bounds(self, bounds, zoom):
        """
        Return all tiles intersecting with bounds.

        Bounds values will be cleaned if they cross the antimeridian or are
        outside of the Northern or Southern tile pyramid bounds.

        Parameters
        ----------
        bounds : tuple
            (left, bottom, right, top) bounding values in tile pyramid CRS
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        for tile in self.tiles_from_bbox(box(*bounds), zoom):
            yield self.tile(*tile.id)

    def tiles_from_bbox(self, geometry, zoom):
        """
        All metatiles intersecting with given bounding box.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        for tile in self.tile_pyramid.tiles_from_bbox(geometry, zoom):
            yield self.tile(*tile.id)

    def tiles_from_geom(self, geometry, zoom):
        """
        Return all tiles intersecting with input geometry.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : ``BufferedTile``
        """
        for tile in self.tile_pyramid.tiles_from_geom(geometry, zoom):
            yield self.tile(*tile.id)

    def intersecting(self, tile):
        """
        Return all BufferedTiles intersecting with tile.

        Parameters
        ----------
        tile : ``BufferedTile``
            another tile
        """
        return [
            self.tile(*intersecting_tile.id)
            for intersecting_tile in self.tile_pyramid.intersecting(tile)]


class BufferedTile(Tile):
    """
    A special tile with fixed pixelbuffer.

    Parameters
    ----------
    tile : ``Tile``
    pixelbuffer : integer
        tile buffer in pixels

    Attributes
    ----------
    height : integer
        tile height in pixels
    width : integer
        tile width in pixels
    shape : tuple
        tile width and height in pixels
    affine : ``Affine``
        ``Affine`` object describing tile extent and pixel size
    bounds : tuple
        left, bottom, right, top values of tile boundaries
    bbox : ``shapely.geometry``
        tile bounding box as shapely geometry
    pixelbuffer : integer
        pixelbuffer used to create tile
    profile : dictionary
        rasterio metadata profile
    """

    def __init__(self, tile, pixelbuffer=0):
        """Initialize."""
        assert not isinstance(tile, BufferedTile)
        Tile.__init__(self, tile.tile_pyramid, tile.zoom, tile.row, tile.col)
        self._tile = tile
        self.pixelbuffer = pixelbuffer
        self.left = self.bounds.left
        self.bottom = self.bounds.bottom
        self.right = self.bounds.right
        self.top = self.bounds.top

    @cached_property
    def height(self):
        """Return buffered height."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).height

    @cached_property
    def width(self):
        """Return buffered width."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).width

    @cached_property
    def shape(self):
        """Return buffered shape."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer)

    @cached_property
    def affine(self):
        """Return buffered Affine."""
        return self._tile.affine(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bounds(self):
        """Return buffered bounds."""
        return self._tile.bounds(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bbox(self):
        """Return buffered bounding box."""
        return self._tile.bbox(pixelbuffer=self.pixelbuffer)

    def get_children(self):
        """
        Get tile children (intersecting tiles in next zoom level).

        Returns
        -------
        children : list
            a list of ``BufferedTiles``
        """
        return [BufferedTile(t, self.pixelbuffer) for t in self._tile.get_children()]

    def get_parent(self):
        """
        Get tile parent (intersecting tile in previous zoom level).

        Returns
        -------
        parent : ``BufferedTile``
        """
        return BufferedTile(self._tile.get_parent(), self.pixelbuffer)

    def get_neighbors(self, connectedness=8):
        """
        Return tile neighbors.

        Tile neighbors are unique, i.e. in some edge cases, where both the left
        and right neighbor wrapped around the antimeridian is the same. Also,
        neighbors ouside the northern and southern TilePyramid boundaries are
        excluded, because they are invalid.

        -------------
        | 8 | 1 | 5 |
        -------------
        | 4 | x | 2 |
        -------------
        | 7 | 3 | 6 |
        -------------

        Parameters
        ----------
        connectedness : int
            [4 or 8] return four direct neighbors or all eight.

        Returns
        -------
        list of BufferedTiles
        """
        return [
            BufferedTile(t, self.pixelbuffer)
            for t in self._tile.get_neighbors(connectedness=connectedness)
        ]

    def is_on_edge(self):
        """Determine whether tile touches or goes over pyramid edge."""
        return (
            self.left <= self.tile_pyramid.left or      # touches_left
            self.bottom <= self.tile_pyramid.bottom or  # touches_bottom
            self.right >= self.tile_pyramid.right or    # touches_right
            self.top >= self.tile_pyramid.top           # touches_top
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.pixelbuffer == other.pixelbuffer and
            self.tp == other.tp and
            self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'BufferedTile(%s, tile_pyramid=%s, pixelbuffer=%s)' % (
            self.id, self.tp, self.pixelbuffer
        )

    def __hash__(self):
        return hash(repr(self))
