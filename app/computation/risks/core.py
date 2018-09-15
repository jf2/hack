from enum import Enum

class RiskType(Enum):
    """ The type of risk """
    INVALID = 1
    FIRE = 2
    FLOODING = 3
    #EARTHQUAKE = 4

class Risk:
    """ A risk """

    # general
    risk_type = RiskType.INVALID

    # region of interest
    
    def __init__(self, risk_type):
        self.risk_type = risk_type
        self.range_min = 0
        self.range_max = 1
        self.value = -1

    def get_risk_score(self, lon, lat, radius):
        return self.value