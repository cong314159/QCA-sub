from QCAInputSim import *
import os
import numpy as np


if __name__ == '__main__':
    subHome = os.getcwd()
    # simHome = "/home/congj/code/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"
    # simHome = "/Users/joe/dev/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"
    simHome = "/home/joe/dev/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"

    job = 'calculation'
    circuitType = 'inverse'
    mission = 'clockWL'
    minValue = 10.0
    maxValue = 401.0
    step = 10.0

    calcLog = open(simHome + '/' + 'calcLog', 'w')

    for parameter in np.arange(minValue, maxValue, step):
        if circuitType not in ['fanin', 'fanout', 'inverse', 'input']:
            raise ValueError('circuit type error')

        if job not in ['calculation', 'visualization']:
            raise ValueError('job type error')

        if mission == 'section':
            calc = Calculation(simHome, job, circuitType=circuitType, section=parameter)
        elif mission == 'overlap':
            calc = Calculation(simHome, job, circuitType=circuitType, overlap=parameter)
        elif mission == 'clockWL':
            calc = Calculation(simHome, job, circuitType=circuitType, clockWL=parameter, section=20)
        elif mission == 'invIdx':
            calc = Calculation(simHome, job, circuitType=circuitType, invIdx=parameter)
        else:
            raise ValueError('mission type error')

        calc.getDirName()
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

        if calc.job == "visualization":
            os.chdir(calc.path)
            os.system("matlab < calculation.m")
            os.chdir(subHome)

    calcLog.close()