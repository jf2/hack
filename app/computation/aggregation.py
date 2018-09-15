from risks.core import Risk, RiskType
from risks.specializations import *

def meanOfAll():
    """ get mean of all available risk factors """

    mean = 0
    count = 0
    lon = 0.0
    lat = 0.0
    radius = 0

    for risk_type in RiskType:
        if risk_type is not RiskType.INVALID:
            count += 1
            risk_special = risk_factory(risk_type)
            mean += risk_special.get_risk_score(lon, lat, radius)
            
            print(risk_type, risk_special.get_risk_score(lon, lat, radius))

    mean /= count

    print("Risk mean value is: ")
    print(mean)

def get_risk_score_by_type(risk_type, lon, lat, radius):
    risk_special = risk_factory(risk_type)
    return risk_special.get_risk_score(lon, lat, radius)

if __name__ == '__main__':
    """ entry point for testing """
    print("started")
    meanOfAll()
    #print("fire risk is", get_risk_score_by_type(RiskType.FIRE, 6.123, 7.123, 1000))
    #print("flooding risk is", get_risk_score_by_type(RiskType.FLOODING, 6.123, 7.123, 1000))
    print("finished")