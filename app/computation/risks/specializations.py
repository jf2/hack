from risks.core import *
import ee

class RiskFire(Risk):
    """ Fire risk """

    def __init__(self):
        startDate = '2007-01-01'
        endDate = '2018-01-01'
        self.risk_type = RiskType.FIRE
        ee.Initialize()
        image_data = ee.ImageCollection('FIRMS').filter(ee.Filter.date(startDate, endDate))
        fire_band_data = image_data.select('T21')

    def getRiskScore(self, lon, lat, radius):
        return 0.5