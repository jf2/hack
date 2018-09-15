from risks.core import Risk, RiskType
from risks.specializations import *
from risks.utilities import *

def meanOfAll(lon, lat, radius):
    """ get mean of all available risk factors """

    mean = 0
    count = 0

    for risk_type in RiskType:
        if risk_type is not RiskType.INVALID:
            count += 1
            risk_special = risk_factory(risk_type)
            mean += risk_special.get_risk_score(lon, lat, radius)
            
            print(risk_type, risk_special.get_risk_score(lon, lat, radius))

    mean /= count

    print("Risk mean value is:", mean)

def get_risk_score_by_type(risk_type, lon, lat, radius):
    risk_special = risk_factory(risk_type)
    return risk_special.get_risk_score(lon, lat, radius)

if __name__ == '__main__':
    """ entry point for testing """
    #print("started")
    lon = 89
    lat = 22
    radius = 0.2
    meanOfAll(lon, lat, radius)
    #print("finished")