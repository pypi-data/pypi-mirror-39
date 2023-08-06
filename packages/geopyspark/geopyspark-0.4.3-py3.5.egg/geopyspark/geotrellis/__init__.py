"""This subpackage contains the code that reads, writes, and processes data using GeoTrellis."""
from collections import namedtuple
import json
import warnings
import datetime
import functools
import datetime
from shapely.geometry import box
import pytz

from geopyspark import get_spark_context
from geopyspark.geotrellis.constants import CellType, NO_DATA_INT, Unit


_EPOCH = datetime.datetime.utcfromtimestamp(0)


def _convert_to_unix_time(date_time):
    if date_time.tzinfo:
        return int((date_time.astimezone(pytz.utc) - _EPOCH.replace(tzinfo=pytz.utc)).total_seconds() * 1000)
    else:
        return int((date_time - _EPOCH).total_seconds() * 1000)


def zfactor_lat_lng_calculator(unit):
    """Produces the Scala class, ``ZFactorCalculator`` as a ``JavaObject``.

    The resulting ``ZFactorCalculator`` produced using this method assumes that
    the ``Tile``\s it will be deriving ``zfactor``\s from are in ``LatLng``
    (aka ``epsg:4326``). This caculator can still be used on ``Tile``\s with
    different projections, however, the resulting ``Slope`` calculations may
    be off.

    Args:
        units (str or :class:`~geopyspark.geotrellis.constant.Unit`): The unit of elevation
            in the target layer.

    Returns:
        ``py4j.JavaObject``
    """

    pysc = get_spark_context()
    calculator = pysc._gateway.jvm.geopyspark.geotrellis.\
            ZFactorCalculator.createLatLngZFactorCalculator(Unit(unit).value)

    return calculator

def zfactor_calculator(mapped_zfactors):
    """Produces the Scala class, ``ZFactorCalculator`` as a ``JavaObject``.

    Unlike the ``ZFactorCalculator`` produced in
    :meth:`~geopyspark.geotrellis.zfactor_lat_lng_calculator`, this resulting
    ``ZFactorCalculator`` can used on ``Tile``\s in a different projection. However,
    it cannot be used between different types of projections. For example, a
    ``ZFactorCalculator`` produced for a Layer that is in ``WebMercator`` will not
    create an accurate ``ZFactor`` for a Layer that is in ``LatLng``.

    Args:
        mapped_zfactors(dict): A ``dict`` that maps lattitudes to ``ZFactor``\s.
           It is not required to supply a mapping for ever lattitude intersected
           in the layer. Rather, based on the lattitudes given, a linear interpolation
           will be performed and any lattitude not mapped will have its ``ZFactor``
           derived from that interpolation.

    Returns:
        ``py4j.JavaObject``
    """

    pysc = get_spark_context()
    string_map = {str(k): str(v) for k, v in mapped_zfactors.items()}
    calculator = pysc._gateway.jvm.geopyspark.geotrellis.\
            ZFactorCalculator.createZFactorCalculator(json.dumps(string_map))

    return calculator


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning) #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)

    return new_func


def crs_to_proj4(crs):
    """Converts a given CRS to a Proj4 string.

    Args:
        crs (str or int): Target CRS of reprojection. Either EPSG code, well-known name, or a
            PROJ.4 string. If ``None``, no reproject will be perfomed.

    Returns:
        str
    """

    if not isinstance(crs, str):
        crs = str(crs)

    pysc = get_spark_context()
    scala_crs = pysc._gateway.jvm.geopyspark.geotrellis.TileLayer.getCRS(crs).get()

    return scala_crs.toProj4String()


def check_layers(base_layer, base_layer_type, layers):
    if not all(isinstance(x, type(base_layer)) for x in layers[1:]):
        raise TypeError("All of the layers to be unioned must be the same type")

    if isinstance(base_layer, RasterLayer):
        return True
    else:
        base_layout = base_layer.layer_metadata.layout_definition.tileLayout
        base_crs = base_layer.layer_metadata.crs

        for layer in layers[1:]:
            layout = layer.layer_metadata.layout_definition.tileLayout
            crs = layer.layer_metadata.crs

            if layout != base_layout or crs != base_crs:
                raise ValueError("The layers to be unioned must have the same TileLayout and CRS")

        return True


class Tile(namedtuple("Tile", 'cells cell_type no_data_value')):
    """Represents a raster in GeoPySpark.

    Note:
        All rasters in GeoPySpark are represented as having multiple bands, even if the original
        raster just contained one.

    Args:
        cells (nd.array): The raster data itself. It is contained within a NumPy array.
        data_type (str): The data type of the values within ``data`` if they were in Scala.
        no_data_value: The value that represents no data value in the raster. This can be
            represented by a variety of types depending on the value type of the raster.

    Attributes:
        cells (nd.array): The raster data itself. It is contained within a NumPy array.
        data_type (str): The data type of the values within ``data`` if they were in Scala.
        no_data_value: The value that represents no data value in the raster. This can be
            represented by a variety of types depending on the value type of the raster.
    """

    __slots__ = []

    @staticmethod
    def dtype_to_cell_type(dtype):
        """Converts a ``np.dtype`` to the corresponding GeoPySpark ``cell_type``.

        Note:
            ``bool``, ``complex64``, ``complex128``, and ``complex256``, are currently not
            supported ``np.dtype``\s.

        Args:
            dtype (np.dtype): The ``dtype`` of the numpy array.

        Returns:
            str. The GeoPySpark ``cell_type`` equivalent of the ``dtype``.

        Raises:
            TypeError: If the given ``dtype`` is not a supported data type.
        """

        name = dtype.name

        if name == 'int8':
            return 'BYTE'
        elif name == 'uint8':
            return 'UBYTE'
        elif name == 'int16':
            return 'SHORT'
        elif name == 'uint16':
            return 'USHORT'
        elif name == 'int32':
            return 'INT'
        elif name in ['uint32', 'float16', 'float32']:
            return 'FLOAT'
        elif name in ['int64', 'uint64', 'float64']:
            return 'DOUBLE'
        else:
            raise TypeError(name, "Is not a supported data type.")

    @classmethod
    def from_numpy_array(cls, numpy_array, no_data_value=None):
        """Creates an instance of ``Tile`` from a numpy array.

        Args:
            numpy_array (np.array): The numpy array to be used to represent the cell values
                of the ``Tile``.

                Note:
                    GeoPySpark does not support arrays with the following data types: ``bool``,
                    ``complex64``, ``complex128``, and ``complex256``.

            no_data_value (optional): The value that represents no data value in the raster.
                This can be represented by a variety of types depending on the value type of
                the raster. If not given, then the value will be ``None``.

        Returns:
            :class:`~geopyspark.geotrellis.Tile`
        """

        return cls(numpy_array, cls.dtype_to_cell_type(numpy_array.dtype), no_data_value)


class Log(object):
    @classmethod
    def debug(cls, pysc, s):
        pysc._gateway.jvm.geopyspark.geotrellis.Log.debug(s)

    @classmethod
    def info(cls, pysc, s):
        pysc._gateway.jvm.geopyspark.geotrellis.Log.info(s)

    @classmethod
    def warn(cls, pysc, s):
        pysc._gateway.jvm.geopyspark.geotrellis.Log.warn(s)

    @classmethod
    def error(cls, pysc, s):
        pysc._gateway.jvm.geopyspark.geotrellis.Log.error(s)


class Extent(namedtuple("Extent", 'xmin ymin xmax ymax')):
    """
    The "bounding box" or geographic region of an area on Earth a raster represents.

    Args:
        xmin (float): The minimum x coordinate.
        ymin (float): The minimum y coordinate.
        xmax (float): The maximum x coordinate.
        ymax (float): The maximum y coordinate.

    Attributes:
        xmin (float): The minimum x coordinate.
        ymin (float): The minimum y coordinate.
        xmax (float): The maximum x coordinate.
        ymax (float): The maximum y coordinate.
    """

    __slots__ = []

    @classmethod
    def from_polygon(cls, polygon):
        """Creates a new instance of ``Extent`` from a Shapely Polygon.

        The new ``Extent`` will contain the min and max coordinates of the Polygon;
        regardless of the Polygon's shape.

        Args:
            polygon (shapely.geometry.Polygon): A Shapely Polygon.

        Returns:
            :class:`~geopyspark.geotrellis.Extent`
        """

        return cls(*polygon.bounds)

    @property
    def to_polygon(self):
        """Converts this instance to a Shapely Polygon.

        The resulting Polygon will be in the shape of a box.

        Returns:
            ``shapely.geometry.Polygon``
        """

        return box(*self)


class ProjectedExtent(namedtuple("ProjectedExtent", 'extent epsg proj4')):
    """Describes both the area on Earth a raster represents in addition to its CRS.

    Args:
        extent (:class:`~geopyspark.geotrellis.Extent`): The area the raster represents.
        epsg (int, optional): The EPSG code of the CRS.
        proj4 (str, optional): The Proj.4 string representation of the CRS.

    Attributes:
        extent (:class:`~geopyspark.geotrellis.Extent`): The area the raster represents.
        epsg (int, optional): The EPSG code of the CRS.
        proj4 (str, optional): The Proj.4 string representation of the CRS.

    Note:
        Either ``epsg`` or ``proj4`` must be defined.
    """

    __slots__ = []

    def __new__(cls, extent, epsg=None, proj4=None):
        return super(ProjectedExtent, cls).__new__(cls, extent, epsg, proj4)

    def _asdict(self):
        if isinstance(self.extent, dict):
            return {'extent': self.extent, 'epsg': self.epsg, 'proj4': self.proj4}
        else:
            return {'extent': self.extent._asdict(), 'epsg': self.epsg, 'proj4': self.proj4}


class TemporalProjectedExtent(namedtuple("TemporalProjectedExtent", 'extent instant epsg proj4')):
    """Describes the area on Earth the raster represents, its CRS, and the time the data was
    collected.

    Args:
        extent (:class:`~geopyspark.geotrellis.Extent`): The area the raster represents.
        instant (``datetime.datetime``): The time stamp of the raster.
        epsg (int, optional): The EPSG code of the CRS.
        proj4 (str, optional): The Proj.4 string representation of the CRS.

    Attributes:
        extent (:class:`~geopyspark.geotrellis.Extent`): The area the raster represents.
        instant (``datetime.datetime``): The time stamp of the raster.
        epsg (int, optional): The EPSG code of the CRS.
        proj4 (str, optional): The Proj.4 string representation of the CRS.

    Note:
        Either ``epsg`` or ``proj4`` must be defined.
    """

    __slots__ = []

    def __new__(cls, extent, instant, epsg=None, proj4=None):
        return super(TemporalProjectedExtent, cls).__new__(cls, extent, instant, epsg, proj4)

    def _asdict(self):
        if isinstance(self.extent, dict):
            return {'extent': self.extent, 'instant': self.instant, 'epsg': self.epsg,
                    'proj4': self.proj4}
        else:
            return {'extent': self.extent._asdict(), 'instant': self.instant, 'epsg': self.epsg,
                    'proj4': self.proj4}


class GlobalLayout(namedtuple("GlobalLayout", 'tile_size zoom threshold')):
    """TileLayout type that spans global CRS extent.

    When passed in place of LayoutDefinition it signifies that a LayoutDefinition instance should be
    constructed such that it fits the global CRS extent. The cell resolution of resulting layout will
    be one of resolutions implied by power of 2 pyramid for that CRS. Tiling to this layout will
    likely result in either up-sampling or down-sampling the source raster.

    Args:
        tile_size (int): The number of columns and row pixels in each tile.
        zoom (int, optional): Override the zoom level in power of 2 pyramid.
        threshold(float, optional): The percentage difference between a cell size and a zoom level and
            the resolution difference between that zoom level and the next that is tolerated to snap to
            the lower-resolution zoom level. For example, if this paramter is 0.1, that means we're
            willing to downsample rasters with a higher resolution in order to fit them to some zoom
            level Z, if the difference is resolution is less than or equal to 10% the difference between
            the resolutions of zoom level Z and zoom level Z+1.

    Attributes:
        tile_size (int): The number of columns and row pixels in each tile.
        zoom (int): The desired zoom level of the layout.
        threshold(float, optional): The percentage difference between a cell size and a zoom level and
            the resolution difference between that zoom level and the next that is tolerated to snap to
            the lower-resolution zoom level.
    """

    __slots__ = []

    def __new__(cls, tile_size=None, zoom=None, threshold=None):
        tile_size = tile_size or 256
        threshold = threshold or 0.1

        return super(cls, GlobalLayout).__new__(cls, tile_size, zoom, threshold)


class LocalLayout(namedtuple("LocalLayout", 'tile_cols tile_rows')):
    """TileLayout type that snaps the layer extent.

    When passed in place of LayoutDefinition it signifies that a LayoutDefinition instances should
    be constructed over the envelope of the layer pixels with given tile size. Resulting TileLayout
    will match the cell resolution of the source rasters.

    Args:
        tile_size (int, optional): The number of columns and row pixels in each tile. If this
            is ``None``, then the sizes of each tile will be set using ``tile_cols`` and
            ``tile_rows``.
        tile_cols (int, optional): The number of column pixels in each tile. This supersedes
            ``tile_size``. Meaning if this and ``tile_size`` are set, then this will be used for
            the number of colunn pixles. If ``None``, then the number of column pixels will
            default to 256.
        tile_rows (int, optional): The number of rows pixels in each tile. This supersedes
            ``tile_size``. Meaning if this and ``tile_size`` are set, then this will be used for
            the number of row pixles. If ``None``, then the number of row pixels will
            default to 256.

    Attributes:
        tile_cols (int): The number of column pixels in each tile
        tile_rows (int): The number of rows pixels in each tile. This supersedes
    """

    __slots__ = []

    def __new__(cls, tile_size=None, tile_cols=None, tile_rows=None):
        tile_cols = tile_cols or tile_size or 256
        tile_rows = tile_rows or tile_size or 256

        return super(cls, LocalLayout).__new__(cls, tile_cols, tile_rows)


class TileLayout(namedtuple("TileLayout", 'layoutCols layoutRows tileCols tileRows')):
    """
    Describes the grid in which the rasters within a Layer should be laid out.

    Args:
        layoutCols (int): The number of columns of rasters that runs east to west.
        layoutRows (int): The number of rows of rasters that runs north to south.
        tileCols (int): The number of columns of pixels in each raster that runs east to west.
        tileRows (int): The number of rows of pixels in each raster that runs north to south.

    Attributes:
        layoutCols (int): The number of columns of rasters that runs east to west.
        layoutRows (int): The number of rows of rasters that runs north to south.
        tileCols (int): The number of columns of pixels in each raster that runs east to west.
        tileRows (int): The number of rows of pixels in each raster that runs north to south.
    """

    __slots__ = []


class LayoutDefinition(namedtuple("LayoutDefinition", 'extent tileLayout')):
    """
    Describes the layout of the rasters within a Layer and how they are projected.

    Args:
        extent (:class:`~geopyspark.geotrellis.Extent`): The ``Extent`` of the layout.
        tileLayout (:class:`~geopyspark.geotrellis.TileLayout`): The ``TileLayout`` of
            how the rasters within the Layer.

    Attributes:
        extent (:class:`~geopyspark.geotrellis.Extent`): The ``Extent`` of the layout.
        tileLayout (:class:`~geopyspark.geotrellis.TileLayout`): The ``TileLayout`` of
            how the rasters within the Layer.
    """

    __slots__ = []


class SpatialKey(namedtuple("SpatialKey", 'col row')):
    """
    Represents the position of a raster within a grid.
    This grid is a 2D plane where raster positions are represented by a pair of coordinates.

    Args:
        col (int): The column of the grid, the numbers run east to west.
        row (int): The row of the grid, the numbers run north to south.

    Attributes:
        col (int): The column of the grid, the numbers run east to west.
        row (int): The row of the grid, the numbers run north to south.
    """

    __slots__ = []


class SpaceTimeKey(namedtuple("SpaceTimeKey", 'col row instant')):
    """
    Represents the position of a raster within a grid.
    This grid is a 3D plane where raster positions are represented by a pair of coordinates as well
    as a z value that represents time.

    Args:
        col (int): The column of the grid, the numbers run east to west.
        row (int): The row of the grid, the numbers run north to south.
        instant (``datetime.datetime``): The time stamp of the raster.

    Attributes:
        col (int): The column of the grid, the numbers run east to west.
        row (int): The row of the grid, the numbers run north to south.
        instant (``datetime.datetime``): The time stamp of the raster.
    """

    __slots__ = []


class RasterizerOptions(namedtuple("RasterizerOption", 'includePartial sampleType')):
    """Represents options available to geometry rasterizer

    Args:
        includePartial (bool, optional): Include partial pixel intersection (default: True)
        sampleType (str, optional): 'PixelIsArea' or 'PixelIsPoint' (default: 'PixelIsPoint')

    Attributes:
        includePartial (bool): Include partial pixel intersection.
        sampleType (str): How the sampling should be performed during rasterization.
    """

    __slots__ = []

    def __new__(cls, includePartial=True, sampleType='PixelIsPoint'):
        return super(cls, RasterizerOptions).__new__(cls, includePartial, sampleType)


class Bounds(namedtuple("Bounds", 'minKey maxKey')):
    """
    Represents the grid that covers the area of the rasters in a Layer on a grid.

    Args:
        minKey (:class:`~geopyspark.geotrellis.SpatialKey` or :class:`~geopyspark.geotrellis.SpaceTimeKey`):
            The smallest ``SpatialKey`` or ``SpaceTimeKey``.
        minKey (:class:`~geopyspark.geotrellis.SpatialKey` or :class:`~geopyspark.geotrellis.SpaceTimeKey`):
            The largest ``SpatialKey`` or ``SpaceTimeKey``.

    Attributes:
        minKey (:class:`~geopyspark.geotrellis.SpatialKey` or :class:`~geopyspark.geotrellis.SpaceTimeKey`):
            The smallest ``SpatialKey`` or ``SpaceTimeKey``.
        minKey (:class:`~geopyspark.geotrellis.SpatialKey` or :class:`~geopyspark.geotrellis.SpaceTimeKey`):
            The largest ``SpatialKey`` or ``SpaceTimeKey``.
    """

    __slots__ = []

    def _asdict(self):
        min_key_dict = self.minKey._asdict()
        max_key_dict = self.maxKey._asdict()

        if 'instant' in min_key_dict.keys():
            min_key_dict['instant'] = _convert_to_unix_time(min_key_dict['instant'])
            max_key_dict['instant'] = _convert_to_unix_time(max_key_dict['instant'])

        return {'minKey': min_key_dict, 'maxKey': max_key_dict}


class HashPartitionStrategy(namedtuple("HashPartitionStrategy", "num_partitions")):
    """Represents a partitioning strategy for a layer that uses Spark's ``HashPartitioner``
    with a set number of partitions.

    Args:
        num_partitions (int, optional): The number of partitions that should be used during
            partitioning. Default is, ``None``. If ``None`` the resulting layer will have
            a ``HashPartitioner`` with the number of partitions being either the same
            as the input layer's, or a number computed by the method.
    """

    __slots__ = []

    def __new__(cls, num_partitions=None):
        return super(cls, HashPartitionStrategy).__new__(cls, num_partitions)


class SpatialPartitionStrategy(namedtuple("SpatialPartitionStrategy", "num_partitions bits")):
    """Represents a partitioning strategy for a layer that uses GeoPySpark's ``SpatialPartitioner``
    with a set number of partitions.

    This partitioner will try and group ``Tile``\s together that are spatially near each other in
    the same partition. In order to do this, each ``Tile`` has their ``Key Index`` calculated
    using the space filling curve index, ``Z-Curve``.

    Args:
        num_partitions (int, optional): The number of partitions that should be used during
            partitioning. Default is, ``None``. If ``None`` the resulting layer will have
            a ``HashPartitioner`` with the number of partitions being either the same
            as the input layer's, or a number computed by the method.
        bits (int, optional): Helps determine how much data should be placed in each
            partition. Default is, ``8``.

            GeoPySpark uses a Z-order curve to determine how values within the layer should
            be grouped. This is done by first finding the ``Key Index`` of a value and then performing a
            bitwise right shift on the resulting index. From the remaining bits, a partition is selected
            such that those indexes with the same remaining bits will be in the same partition.
            Therefore, as the number of bits shifted to the right increases, so then too does the
            group sizes.

    Attributes:
        num_partitions (int): The number of partitions that should be used during
            partitioning.
        bits (int): Determine how much data should be placed in each partition.
    """

    __slots__ = []

    def __new__(cls, num_partitions=None, bits=8):
        return super(cls, SpatialPartitionStrategy).__new__(cls, num_partitions, bits)


class SpaceTimePartitionStrategy(namedtuple("SpaceTimePartitionStrategy", "time_unit num_partitions bits time_resolution")):
    """Represents a partitioning strategy for a layer that uses GeoPySpark's ``SpaceTimePartitioner``
    with a set number of partitions, units of time, and temporal resolution.

    This partitioner will try and group ``Tile``\s together that are spatially and temproally near each other
    in the same partition. In order to do this, each ``Tile`` has their ``Key Index`` calculated
    using the space filling curve index, ``Z-Curve``.

    Note:
        This partitiong strategy will only work on ``SPACETIME`` layers, and will fail if given a ``SPATIAL``
        one. For ``SPATIAL`` layers, please see :class:`~geopyspark.geotrellis.SpatialPartitionStrategy`.

    Args:
        time_unit (str or :class:`~geopyspark.geotrellis.constants.TimeUnit`): Which time
            unit should be used when saving spatial-temporal data. This controls the resolution of
            each index. Meaning, what time intervals are used to seperate each record.
        num_partitions (int, optional): The number of partitions that should be used during
            partitioning. Default is, ``None``. If ``None`` the resulting layer will have
            a ``HashPartitioner`` with the number of partitions being either the same
            as the input layer's, or a number computed by the method.
        bits (int, optional): Helps determine how much data should be placed in each
            partition. Default is, ``8``.

            GeoPySpark uses a Z-order curve to determine how values within the layer should
            be grouped. This is done by first finding the ``Key Index`` of a value and then performing a
            bitwise right shift on the resulting index. From the remaining bits, a partition is selected
            such that those indexes with the same remaining bits will be in the same partition.
            Therefore, as the number of bits shifted to the right increases, so then too does the
            group sizes.
        time_resolution (str or int, optional): Determines how data for each ``time_unit`` should be
            grouped together. By default, no grouping will occur.

            As an example, having a ``time_unit`` of ``WEEKS`` and a ``time_resolution`` of 5 will
            cause the data to be grouped and stored together in units of 5 weeks. If however
            ``time_resolution`` is not specified, then the data will be grouped and stored in units
            of single weeks.

            This value can either be an ``int`` or a string representation of an ``int``.

    Attributes:
        time_unit (str or :class:`~geopyspark.geotrellis.constants.TimeUnit`): Which time
            unit should be used when saving spatial-temporal data.
        num_partitions (int): The number of partitions that should be used during
            partitioning.
        bits (int): Helps determine how much data should be placed in each
            partition.
        time_resolution (str or int): Determines how data for each ``time_unit`` should be
            grouped together.
    """

    __slots__ = []

    def __new__(cls, time_unit, num_partitions=None, bits=8, time_resolution=None):
        return super(cls, SpaceTimePartitionStrategy).__new__(cls, time_unit, num_partitions, bits, time_resolution)


class Metadata(object):
    """Information of the values within a ``RasterLayer`` or ``TiledRasterLayer``.
    This data pertains to the layout and other attributes of the data within the classes.

    Args:
        bounds (:class:`~geopyspark.geotrellis.Bounds`): The ``Bounds`` of the
            values in the class.
        crs (str or int): The ``CRS`` of the data. Can either be the EPSG code, well-known name, or
            a PROJ.4 projection string.
        cell_type (str or :class:`~geopyspark.geotrellis.constants.CellType`): The data type of the
            cells of the rasters.
        extent (:class:`~geopyspark.geotrellis.Extent`): The ``Extent`` that covers
            the all of the rasters.
        layout_definition (:class:`~geopyspark.geotrellis.LayoutDefinition`): The
            ``LayoutDefinition`` of all rasters.

    Attributes:
        bounds (:class:`~geopyspark.geotrellis.Bounds`): The ``Bounds`` of the values in the class.
        crs (str or int): The CRS of the data. Can either be the EPSG code, well-known name, or
            a PROJ.4 projection string.
        cell_type (str): The data type of the cells of the rasters.
        no_data_value (int or float or None): The noData value of the rasters within the layer.
            This can either be ``None``, an ``int``, or a ``float`` depending on the ``cell_type``.
        extent (:class:`~geopyspark.geotrellis.Extent`): The ``Extent`` that covers
            the all of the rasters.
        tile_layout (:class:`~geopyspark.geotrellis.TileLayout`): The ``TileLayout``
            that describes how the rasters are orginized.
        layout_definition (:class:`~geopyspark.geotrellis.LayoutDefinition`): The
            ``LayoutDefinition`` of all rasters.
    """

    def __init__(self, bounds, crs, cell_type, extent, layout_definition):
        self.bounds = bounds
        self.crs = crs

        if isinstance(cell_type, CellType):
            self.cell_type = CellType(cell_type).value
        else:
            self.cell_type = cell_type

        self.extent = extent
        self.tile_layout = layout_definition.tileLayout
        self.layout_definition = layout_definition

        if 'raw' in self.cell_type or 'bool' in self.cell_type:
            self.no_data_value = None
        elif 'ud' in self.cell_type:
            value = self.cell_type.split("ud")[1]

            if "float" in self.cell_type:
                self.no_data_value = float(value)
            else:
                self.no_data_value = int(value)
        else:
            if self.cell_type == CellType.INT8.value:
                self.no_data_value = -128
            elif self.cell_type == CellType.UINT8.value or self.cell_type == CellType.UINT16.value:
                self.no_data_value = 0
            elif self.cell_type == CellType.INT16.value:
                self.no_data_value = -32768
            elif self.cell_type == CellType.INT32.value:
                self.no_data_value = NO_DATA_INT
            else:
                self.no_data_value = float('nan')

    @classmethod
    def from_dict(cls, metadata_dict):
        """Creates ``Metadata`` from a dictionary.

        Args:
            metadata_dict (dict): The ``Metadata`` of a ``RasterLayer`` or ``TiledRasterLayer``
                instance that is in ``dict`` form.

        Returns:
            :class:`~geopyspark.geotrellis.Metadata`
        """

        crs = metadata_dict['crs']
        cell_type = metadata_dict['cellType']

        bounds_dict = metadata_dict['bounds']

        if len(bounds_dict['minKey']) == 2:
            min_key = SpatialKey(**bounds_dict['minKey'])
            max_key = SpatialKey(**bounds_dict['maxKey'])
        else:
            scala_min_key = bounds_dict['minKey']
            scala_max_key = bounds_dict['maxKey']

            scala_min_key['instant'] = datetime.datetime.utcfromtimestamp(scala_min_key['instant'] / 1000)
            scala_max_key['instant'] = datetime.datetime.utcfromtimestamp(scala_max_key['instant'] / 1000)

            min_key = SpaceTimeKey(**scala_min_key)
            max_key = SpaceTimeKey(**scala_max_key)

        bounds = Bounds(min_key, max_key)
        extent = Extent(**metadata_dict['extent'])

        layout_definition = LayoutDefinition(
            Extent(**metadata_dict['layoutDefinition']['extent']),
            TileLayout(**metadata_dict['layoutDefinition']['tileLayout']))

        return cls(bounds, crs, cell_type, extent, layout_definition)

    def to_dict(self):
        """Converts this instance to a ``dict``.

        Returns:
            ``dict``
        """

        metadata_dict = {
            'bounds': self.bounds._asdict(),
            'crs': self.crs,
            'cellType': self.cell_type,
            'extent': self.extent._asdict(),
            'layoutDefinition': {
                'extent': self.layout_definition.extent._asdict(),
                'tileLayout': self.tile_layout._asdict()
            }
        }

        return metadata_dict

    def __repr__(self):
        return "Metadata({}, {}, {}, {}, {}, {}, {})".format(self.bounds, self.cell_type,
                                                             self.no_data_value, self.crs,
                                                             self.extent, self.tile_layout,
                                                             self.layout_definition)


    def __str__(self):
        return ("Metadata("
                "bounds={}"
                "cellType={}"
                "noDataValue={}"
                "crs={}"
                "extent={}"
                "tileLayout={}"
                "layoutDefinition={})").format(self.bounds, self.cell_type,
                                               self.no_data_value, self.crs, self.extent,
                                               self.tile_layout, self.layout_definition)


__all__ = ["Tile", "Extent", "ProjectedExtent", "TemporalProjectedExtent", "SpatialKey", "SpaceTimeKey",
           "Metadata", "TileLayout", "GlobalLayout", "LocalLayout", "LayoutDefinition", "Bounds", "RasterizerOptions",
           "zfactor_lat_lng_calculator", "zfactor_calculator", "HashPartitionStrategy", "SpatialPartitionStrategy",
           "SpaceTimePartitionStrategy"]

from . import catalog
from . import color
from . import constants
from . import converters
from . import geotiff
from . import rasterio
from . import histogram
from . import layer
from . import neighborhood
from . import tms

from .catalog import *
from .color import *
from .constants import *
from .converters import *
from .cost_distance import *
from .euclidean_distance import *
from .hillshade import *
from .histogram import *
from .layer import *
from .neighborhood import *
from .rasterize import *
from .tms import *
from .union import *
from .combine_bands import *

__all__ += catalog.__all__
__all__ += color.__all__
__all__ += constants.__all__
__all__ += ['cost_distance']
__all__ += ['euclidean_distance']
__all__ += ['geotiff']
__all__ += ['rasterio']
__all__ += ['hillshade']
__all__ += histogram.__all__
__all__ += layer.__all__
__all__ += neighborhood.__all__
__all__ += ['rasterize', 'rasterize_features']
__all__ += tms.__all__
__all__ += ['union']
__all__ += ['combine_bands']
