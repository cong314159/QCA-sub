import os
import numpy as np


class Calculation:
    def __init__(self, *args, **kwargs):
        self.homeDir = args[0]
        self.job = args[1]

        self.algorithm = 'ICH'
        if 'algorithm' in kwargs:
            self.algorithm = kwargs.get('algorithm')

        self.circuitType = 'BitPacket'
        if 'circuitType' in kwargs:
            self.circuitType = kwargs.get('circuitType')

        self.section = 7
        if 'section' in kwargs:
            self.section = kwargs.get('section')

        self.overlap = 3
        if 'overlap' in kwargs:
            self.overlap = kwargs.get('overlap')

        self.invIdx = 7
        if (self.circuitType == 'inverse') & ('invIdx' in kwargs):
            self.invIdx = kwargs.get('invIdx')

        self.radiusOfEffect = 10.1
        if 'radiusOfEffect' in kwargs:
            self.radiusOfEffect = kwargs.get('radiusOfEffect')

        self.numOfPeriods = 6
        if 'numOfPeriods' in kwargs:
            self.numOfPeriods = kwargs.get('numOfPeriods')

        self.cellSpacing = 2.0
        if 'cellSpacing' in kwargs:
            self.cellSpacing = kwargs.get('cellSpacing')

        self.clockWL = 50.0
        if 'clockWL' in kwargs:
            self.clockWL = kwargs.get('clockWL')

        self.clockAmp = 20.0
        if 'clockAmp' in kwargs:
            self.clockAmp = kwargs.get('clockAmp')

        self.clockPeriod = 200
        if 'clockPeriod' in kwargs:
            self.clockPeriod = kwargs.get('clockPeriod')

        self.inputWL = 50.0
        if 'inputWL' in kwargs:
            self.inputWL = kwargs.get('inputWL')

        self.inputType = 'Fermi'
        if 'inputType' in kwargs:
            self.inputType = kwargs.get('inputType')

        self.inputAmp = 0.3
        if 'inputAmp' in kwargs:
            self.inputAmp = kwargs.get('inputAmp')

        self.inputMean = 0.15
        if 'inputMean' in kwargs:
            self.inputMean = kwargs.get('inputMean')

        self.inputShrp = 1.0
        if 'inputShrp' in kwargs:
            self.inputShrp = kwargs.get('inputShrp')

        self.inputPhs = 0.25
        if 'inputPhs' in kwargs:
            self.inputPhs = kwargs.get('inputPhs')

        self.tspp = 200
        if 'tspp' in kwargs:
            self.tspp = kwargs.get('tspp')

        self.name = self.getName()
        self.path = self.getDirName()

    def getName(self):
        name = self.algorithm + '_'

        if self.circuitType == 'inverse':
            name += 'inverse' + str(self.invIdx) + '_'
        else:
            name += self.circuitType + '_'

        name += 'section' + str(self.section) + '_'

        name += 'overlap' + str(self.overlap) + '_'

        name += 'RoE' + str(self.radiusOfEffect) + '_'

        name += 'CS' + str(self.cellSpacing) + '_'

        name += 'ClkWL' + str(self.clockWL) + '_'

        name += 'ClkAmp' + str(self.clockAmp) + '_'

        name += 'InWL' + str(self.inputWL) + '_'

        name += 'InType' + self.inputType + '_'

        name += 'InAmp' + str(self.inputAmp) + '_'

        name += 'InMu' + str(self.inputMean) + '_'

        name += 'InShrp' + str(self.inputShrp) + '_'

        name += 'InPhs' + str(self.inputPhs) + '_'

        name += 'TSPP' + str(self.tspp)

        return name

    def getDirName(self):
        return self.homeDir + self.name

    def makeCalcDir(self):
        os.mkdir(self.path)

    def makeMatlabFile(self):
        header = "calculation/header.txt"
        circuit = "circuit/" + self.circuitType + ".txt"
        signal = "signal/signal.txt"
        workload = "calculation/" + self.job + ".txt"

        with open(header) as fin:
            with open(self.path + '/' + 'calculation.m', 'w+') as fout:
                for line in fin:
                    fout.write(line)

        with open(self.path + '/' + 'calculation.m', 'a+') as fout:
            fout.write("SimulationName = '" + "sim_" + self.circuitType + "_'; \n")
            fout.write("inputType = 'Ctrl'; \n")
            fout.write("epsilon_0 = 8.854E-12; \n")
            fout.write("a=1e-9; %[m] \n")
            fout.write("q=1; %[eV] \n")
            fout.write("Eo = q^2*(1.602e-19)/(4*pi*epsilon_0*a)*(1-1/sqrt(2)); % Kink Energy Field Strength \n")
            fout.write("characteristicLength = 1; % [nm] \n")
            fout.write("lsection = " + str(self.section) + "; \n")
            fout.write("lcross = " + str(self.overlap) + "; \n")
            fout.write("idxInvert = " + str(self.invIdx) + "; \n")
            fout.write("pitch = " + str(self.cellSpacing + 1) + "; \n")
            fout.write("radiusOfEffect = " + str(self.radiusOfEffect) + "; \n")
            fout.write("numOfPeriods = " + str(self.numOfPeriods) + "; \n")
            fout.write("clockSignalPeriod = " + str(self.clockPeriod) + "; \n")
            fout.write("clockSignalAmp = " + str(self.clockAmp) + "; \n")
            fout.write("clockSignalWavelength = " + str(self.clockWL) + "; \n")
            fout.write("inputSignalType = '" + self.inputType + "'; \n")
            fout.write("inputSignalWavelength = " + str(self.inputWL) + "; \n")
            fout.write("inputSignalAmp = " + str(self.inputAmp) + "; \n")
            fout.write("inputSignalPeriod = clockSignalPeriod * 2; \n")
            fout.write("inputSignalSharpness = " + str(self.inputShrp) + "; \n")
            fout.write("inputSignalPhase = " + str(self.inputShrp) + "; \n")
            fout.write("inputSignalMean = inputSignalAmp / 2; \n\n")

        with open(circuit) as fin:
            with open(self.path + '/' + 'calculation.m', 'a+') as fout:
                for line in fin:
                    fout.write(line)

        with open(signal) as fin:
            with open(self.path + '/' + 'calculation.m', 'a+') as fout:
                for line in fin:
                    fout.write(line)

        with open(workload) as fin:
            with open(self.path + '/' + 'calculation.m', 'a+') as fout:
                for line in fin:
                    fout.write(line)

    def makeBashFile(self):
        with open("calculation/submission.txt") as fin:
            with open(self.path + '/' + 'calculation.sh', 'w+') as fout:
                for line in fin:
                    fout.write(line)


if __name__ == '__main__':
    subHome = os.getcwd()
    # simHome = "/home/congj/code/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"
    simHome = "/Users/joe/dev/matlab/QCAInputSim/Simulations/ICH_WindowOfOperation_study/"

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

    calcLog.close()



