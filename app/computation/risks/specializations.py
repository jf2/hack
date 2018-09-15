from risks.core import Risk, RiskType
from risks.utilities import *
import ee
import numpy as np

def risk_factory(risk_type):
    """ factory to create risk specializations """
    if risk_type == RiskType.FIRE: return RiskFire()
    if risk_type == RiskType.FLOODING: return RiskFlooding()

    assert 0, "unsupported risk type: %s" % risk_type

class RiskFire(Risk):
    """ Fire risk """

    risk_type = RiskType.FIRE

    def __init__(self):
        self.start_date = '2015-01-01'
        self.end_date = '2018-01-01'
        self.dataset_name = 'FIRMS'
        self.dataset_band_name = 'T21'
        self.range_min = 300
        self.range_max = 510
        
        # get band of image collection
        ee.Initialize()
        self.image_collection = ee.ImageCollection(self.dataset_name).\
            filter(ee.Filter.date(self.start_date, self.end_date)).\
            select(self.dataset_band_name)

    def get_risk_score(self, lon, lat, radius):

        self.nparray = image_coll_to_np_array(self.image_collection, 
            lon, lat, radius)

        self.nparray = map_linearly_from(self.nparray, 
            self.range_min, self.range_max)

        return np.mean(self.nparray)

class RiskFlooding(Risk):
    """ Flooding risk """

    risk_type = RiskType.FIRE

    def __init__(self):
        self.start_date = '2007-01-01'
        self.end_date = '2018-01-01'
        self.dataset_name = 'MODIS/006/MOD44W'
        self.dataset_band_name = 'water_mask'
        self.range_min = 0.0
        self.range_max = 1.0
        
        # get band of image collection
        ee.Initialize()
        self.image_collection = ee.ImageCollection(self.dataset_name).\
            filter(ee.Filter.date(self.start_date, self.end_date)).\
            select(self.dataset_band_name)

    def get_risk_score(self, lon, lat, radius):

        self.nparray = image_coll_to_np_array(self.image_collection, 
            lon, lat, radius)

        #print("shape")
        #print(self.nparray.shape)
        #print("entries")
        #print(self.nparray)

        return np.mean(self.nparray)