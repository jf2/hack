from enum import Enum

class RiskType(Enum):
    """ The type of risk """
    INVALID = 1
    FIRE = 2
    FLOODING = 3
    EARTHQUAKE = 4

class Risk:
    """ A risk """

    severity = -1

    risk_type = RiskType.INVALID
    rangeMin = 0
    rangeMax = 1
    value = -1

    def __init__(self, risk_type):
        self.risk_type = risk_type