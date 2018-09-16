# Import the Earth Engine Python Package
import ee
import numpy as np

# Initialize the Earth Engine object, using the authentication credentials.
ee.Initialize()

if __name__ == "__main__":
    # Print the information for an image asset.
    # image = ee.Image('srtm90_v4')
    # print(image.getInfo())

    ee.Initialize()

    noa = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012')
    lonlat_noa = ee.Image.pixelLonLat().addBands(noa)
    roi = ee.Geometry.Point([8.55, 47.37]).buffer(20000)
    noa_clipped = lonlat_noa.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=100)
    noa_clipped_getinfo = noa_clipped.getInfo()
    result = np.c_[noa_clipped_getinfo['longitude'], noa_clipped_getinfo['latitude'], noa_clipped_getinfo['avg_vis']]
