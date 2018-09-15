from risks.core import Risk, RiskType
import ee

def risk_factory(risk_type):
    """ factory to create risk specializations """
    if risk_type == RiskType.FIRE: return RiskFire()
    if risk_type == RiskType.FLOODING: return RiskFlooding()

    assert 0, "unsupported risk type: %s" % risk_type

class RiskFire(Risk):
    """ Fire risk """

    def __init__(self):
        startDate = '2007-01-01'
        endDate = '2018-01-01'
        self.risk_type = RiskType.FIRE
        ee.Initialize()
        image_data = ee.ImageCollection('FIRMS').filter(ee.Filter.date(startDate, endDate))
        fire_band_data = image_data.select('T21')

    def get_risk_score(self, lon, lat, radius):
        return 0.5

class RiskFlooding(Risk):
    """ Flooding risk """

    def __init__(self):
        startDate = '2007-01-01'
        endDate = '2018-01-01'
        self.risk_type = RiskType.FIRE
        ee.Initialize()

    def get_risk_score(self, lon, lat, radius):
        return 3.5