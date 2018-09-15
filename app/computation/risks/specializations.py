from risks.core import Risk, RiskType
import ee
import numpy as np
#import matplotlib.pyplot as plt        

def risk_factory(risk_type):
    """ factory to create risk specializations """
    if risk_type == RiskType.FIRE: return RiskFire()
    if risk_type == RiskType.FLOODING: return RiskFlooding()

    assert 0, "unsupported risk type: %s" % risk_type

class RiskFire(Risk):
    """ Fire risk """

    risk_type = RiskType.FIRE

    def __init__(self):
        self.startDate = '2015-01-01'
        self.endDate = '2018-01-01'
        
        # get band of image collection
        ee.Initialize()
        self.image_collection = ee.ImageCollection('FIRMS').\
        filter(ee.Filter.date(self.startDate, self.endDate)).select('T21')

    def get_risk_score(self, lon, lat, radius):

        # Make an Array Image, with a 1-D Array per pixel.

        self.geometry = ee.Geometry.Rectangle([
            lon - radius, 
            lat - radius, 
            lon + radius, 
            lat + radius])

        # reduce to image reduce to region of image
        self.img_reduced = self.image_collection.reduce(ee.Reducer.mean()).reduceRegion(
            reducer=ee.Reducer.toList(),
            geometry=self.geometry,
            scale=1000)

        # convert to np array
        self.array = ee.Array(self.img_reduced.toArray())
        self.nparray = np.array(self.array.getInfo())

        #print("array shape:", self.array.length())
        print("nparray shape:", self.nparray.shape)

        return 0.5

class RiskFlooding(Risk):
    """ Flooding risk """

    risk_type = RiskType.FIRE

    def __init__(self):
        self.startDate = '2007-01-01'
        self.endDate = '2018-01-01'
        
        # get iamge
        ee.Initialize()
        # todo


    def get_risk_score(self, lon, lat, radius):
        return 3.5