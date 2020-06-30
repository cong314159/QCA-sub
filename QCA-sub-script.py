from QCAInputSim import *
import os
import socket
import numpy as np


if __name__ == '__main__':
    subHome = os.getcwd()
    if socket.gethostname() == "NewBookXL.local":
        simHome = "/Users/joe/dev/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"
    else:
        simHome = "/home/congj/code/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"

    kodiak = True
    algorithm = 'ICH'
    inputType = 'drv'
    calculation = True
    visualization = True
    circuitType = 'majority'
    runningParameter = 'clockWL'
    staticParameter = 'clockAmp'
    staticValue = 20.0
    minValue = 10.0
    maxValue = 401.0
    step = 10.0

    calcLog = open(simHome + '/' + 'calcLog', 'w')

    for parameter in np.arange(minValue, maxValue, step):
        if circuitType not in ['fanin', 'fanout', 'inverse', 'input', 'majority']:
            raise ValueError('circuit type error')

        if (not calculation) & (not visualization):
            raise ValueError('job type error')

        calc = Calculation(simHome,
                           calculation,
                           visualization,
                           groupIdentifier="majority_clockAmpVsWL",
                           algorithm=algorithm,
                           runningParameter=runningParameter,
                           staticParameter=staticParameter,
                           staticValue=staticValue,
                           step=step,
                           minValue=minValue,
                           maxValue=maxValue,
                           circuitType=circuitType,
                           inputType=inputType,
                           clockAmp=staticValue,
                           clockWL=parameter,
                           section=10,
                           tspp=200,
                           offset=10.0,
                           separation=5,
                           numOfPeriods=16,
                           driverActivation=1.0,
                           driverSignalShrp=1.0,
                           driverSignalPhs=0.25,
                           kodiak=True)

        # calc.getDirName()
        calcLog.write(calc.groupName + '\n')
        calcLog.write(calc.name + '\n')

        try:
            calc.makeCalcDir()
        except Exception:
            print('calculation folder already exist')

        try:
            calc.makeMatlabFile()
        except Exception:
            raise RuntimeError('matlab file generation error')

        try:
            calc.makeBashFile()
        except Exception:
            raise RuntimeError('bash file generation error')

        if not calc.kodiak:
            os.chdir(calc.path)
            os.system("matlab < calculation.m -nosplash -nodisplay")
            os.chdir(subHome)

    calcLog.close()