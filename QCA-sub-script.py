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
    inputType = 'ctrl'
    job = 'calculation_visualization_nodisplay'
    circuitType = 'input'
    runningParameter = 'clockWL'
    staticParameter = 'clockAmp'
    minValue = 10.0
    maxValue = 401.0
    step = 10.0

    calcLog = open(simHome + '/' + 'calcLog', 'w')

    for parameter in np.arange(minValue, maxValue, step):
        if circuitType not in ['fanin', 'fanout', 'inverse', 'input']:
            raise ValueError('circuit type error')

        if job not in ['calculation', 'visualization', 'calculation_visualization_nodisplay']:
            raise ValueError('job type error')

        calc = Calculation(simHome,
                           job,
                           algorithm=algorithm,
                           runningParameter=runningParameter,
                           staticParameter=staticParameter,
                           step=step,
                           minValue=minValue,
                           maxValue=maxValue,
                           circuitType=circuitType,
                           inputType=inputType,
                           clockAmp=19.0,
                           clockWL=parameter,
                           section=7,
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

        if (calc.job == "visualization") & (not calc.kodiak):
            os.chdir(calc.path)
            os.system("matlab < calculation.m -nosplash -nodisplay")
            os.chdir(subHome)

    calcLog.close()