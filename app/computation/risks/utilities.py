from risks.core import Risk, RiskType
import ee
import numpy as np

def image_coll_to_np_array(image_collection, 
    lon, lat, radius):
    
    # region of interest
    geometry = ee.Geometry.Rectangle([
        lon - radius, 
        lat - radius, 
        lon + radius, 
        lat + radius])

    # reduce to image reduce to region of image
    img_reduced = image_collection.reduce(ee.Reducer.mean()).reduceRegion(
        reducer=ee.Reducer.toList(),
        geometry=geometry,
        scale=1000)

    # convert to np array
    ee_array = ee.Array(img_reduced.toArray())
    np_array = np.array(ee_array.getInfo())

    return np_array

def map_linearly_from(np_array, 
    range_min, range_max):

    # map linearly to [0,1]
    np_array = np_array - range_min
    np_array = np_array / (range_max - range_min)

    return np_array