from QCAInputSim import *
import os
import socket
import numpy as np


if __name__ == '__main__':
    subHome = os.getcwd()
    if socket.gethostname() == "NewBook":
        simHome = "/Users/joe/dev/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"
    else:
        simHome = "/home/congj/code/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"

    kodiak = True
    algorithm = 'ICH'
    inputType = 'drv_fringing'
    calculation = True
    visualization = True
    circuitType = 'input_3dc'
    runningParameter = 'inputAmp'
    staticParameter = 'clockWL'
    staticValue = 50.0
    minValue = -2.0
    maxValue = 2.1
    step = 0.1

    calcLog = open(simHome + '/' + 'calcLog', 'w')

    for parameter in np.arange(minValue, maxValue, step):
        if circuitType not in ['fanin', 'fanout', 'inverse', 'input', 'input_3dc', 'majority', 'majority_step']:
            raise ValueError('circuit type error')

        if (not calculation) & (not visualization):
            raise ValueError('job type error')

        calc = Calculation(simHome,
                           calculation,
                           visualization,
                           groupIdentifier="input_drv_inputAmp_vs_clockWL_UpdatedRandomizer",
                           algorithm=algorithm,
                           runningParameter=runningParameter,
                           staticParameter=staticParameter,
                           staticValue=staticValue,
                           step=step,
                           minValue=minValue,
                           maxValue=maxValue,
                           circuitType=circuitType,
                           inputType=inputType,
                           clockWL=staticValue,
                           clockAmp=20,
                           section=11,
                           cellSpacing=1.0,
                           tspp=200,
                           inputAmp=parameter,
                           inputSignalType='Exp',
                           # offset=10.0,
                           # separation=10,
                           numOfPeriods=8,
                           driverActivation=1.0,
                           driverSignalShrp=1.0,
                           driverSignalPhs=0.25,
                           FringingParameter=0,
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
