from glob import glob

import gdal, osr, ogr

data_source = '~/Desktop/FF_STATS/maps/LCType.tif'

point = ogr.Geometry(ogr.wkbPoint)

# Specify that the point uses the WGS84 reference system
sr = osr.SpatialReference()
sr.ImportFromEPSG(4326)
point.AssignSpatialReference(sr)

# Point's co-ordinates (in WGS84 it's latitude and longitude)
point.AddPoint(36.16469217, -86.77208918)

def extract_point_from_raster(point, data_source, band_number=1):
    """Return floating-point value that corresponds to given point."""

    # Convert point co-ordinates so that they are in same projection as raster
    point_sr = point.GetSpatialReference()
    raster_sr = osr.SpatialReference()
    raster_sr.ImportFromWkt(data_source.GetProjection())
    transform = osr.CoordinateTransformation(point_sr, raster_sr)
    point.Transform(transform)

    # Convert geographic co-ordinates to pixel co-ordinates
    x, y = point.GetX(-86.77208918), point.GetY(36.16469217)
    forward_transform = Affine.from_gdal(*data_source.GetGeoTransform())
    reverse_transform = ~forward_transform
    px, py = reverse_transform * (x, y)
    px, py = int(px + 0.5), int(py + 0.5)

    # Extract pixel value
    band = data_source.GetRasterBand(band_number)
    structval = band.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_Float32)
    result = struct.unpack('f', structval)[0]
    if result == band.GetNoDataValue():
        result = float('nan')
    return result
