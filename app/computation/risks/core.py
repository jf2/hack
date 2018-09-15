from enum import Enum

class RiskType(Enum):
    """ The type of risk """
    INVALID = 1
    FIRE = 2
    FLOODING = 3
    EARTHQUAKE = 4

class Risk:
    """ A risk """

    # general
    severity = -1
    risk_type = RiskType.INVALID
    range_min = 0
    range_max = 1

    # region of interest
    value = -1

    def __init__(self, risk_type):
        self.risk_type = risk_type

    #def getRiskScore(self, long, lat, radius):
    #    return -1