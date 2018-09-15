from risks.core import *

def meanOfAll():
    """ get mean of all available risk factors """

    mean = 0
    count = 0

    for risk_type in RiskType:
        if risk_type is not RiskType.INVALID:
            count += 1
            risk = Risk(risk_type)
            risk.value = count
            mean += risk.value
            
            print(risk_type, risk.value)

    mean /= count

    print("Mean value is: ")
    print(mean)


if __name__ == '__main__':
    """ entry point for testing """
    print("started")
    meanOfAll()
    print("finished")