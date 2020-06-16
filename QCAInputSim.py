import os
import numpy as np


class Calculation:
    def __init__(self, *args, **kwargs):
        self.homeDir = args[0]
        self.job = args[1]

        self.staticParameter = 'clockAmp'
        if 'staticParameter' in kwargs:
            self.staticParameter = kwargs.get('staticParameter')

        self.runningParameter = 'clockWL'
        if 'runningParameter' in kwargs:
            self.runningParameter = kwargs.get('runningParameter')

        self.minValue = 10.0
        if 'minValue' in kwargs:
            self.minValue = kwargs.get('minValue')

        self.maxValue = 401.0
        if 'maxValue' in kwargs:
            self.maxValue = kwargs.get('maxValue')

        self.step = 10.0
        if 'step' in kwargs:
            self.step = kwargs.get('step')

        self.kodiak = True
        if 'kodiak' in kwargs:
            self.kodiak = kwargs.get('kodiak')

        self.algorithm = 'ICH'
        if 'algorithm' in kwargs:
            self.algorithm = kwargs.get('algorithm')

        self.inputType = 'ctrl'
        if 'inputType' in kwargs:
            self.inputType = kwargs.get('inputType')

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
        if 'invIdx' in kwargs:
            self.invIdx = kwargs.get('invIdx')

        self.offset = 0.0
        if 'offset' in kwargs:
            self.offset = kwargs.get('offset')

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

        self.inputSignalType = 'Fermi'
        if 'inputSignalType' in kwargs:
            self.inputSignalType = kwargs.get('inputSignalType')

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
        self.groupName = self.getGroupName()
        self.path = self.getDirName()

    def getName(self):
        name = self.algorithm + '_'

        name += self.inputType + '_'

        if self.circuitType == 'inverse':
            name += 'inverse' + str(self.invIdx) + '_'
        else:
            name += self.circuitType + '_'

        name += 'section' + str(self.section) + '_'

        name += 'overlap' + str(self.overlap) + '_'

        name += 'offset' + str(self.offset) + '_'

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

    def getGroupName(self):

        name = self.algorithm + '_'

        name += self.inputType + '_'

        if self.circuitType == 'inverse':
            name += 'inverse' + str(self.invIdx) + '_'
        else:
            name += self.circuitType + '_'

        name += self.staticParameter + '_static_'

        name += self.runningParameter + '_running_'

        name += str(self.minValue) + 'min_'

        name += str(self.maxValue) + 'max_'

        name += 'group'

        return name

    def getDirName(self):
        return self.homeDir + self.groupName + '/' + self.name

    def makeCalcDir(self):
        os.makedirs(self.path)

    def makeMatlabFile(self):
        header = "calculation/header.txt"
        circuit = "circuit/" + self.circuitType + '_' + self.inputType + ".txt"
        signal = "signal/signal.txt"
        naming = "calculation/nameAssign.txt"
        workload = "calculation/" + self.job + ".txt"

        with open(header) as file_in:
            with open(self.path + '/' + 'calculation.m', 'w+') as file_out:
                for line in file_in:
                    file_out.write(line)

        with open(self.path + '/' + 'calculation.m', 'a+') as file_out:
            file_out.write("SimulationName = '" + "sim_" + self.circuitType + "_'; \n")
            file_out.write("inputType = 'Ctrl'; \n")
            file_out.write("epsilon_0 = 8.854E-12; \n")
            file_out.write("a=1e-9; %[m] \n")
            file_out.write("q=1; %[eV] \n")
            file_out.write("Eo = q^2*(1.602e-19)/(4*pi*epsilon_0*a)*(1-1/sqrt(2)); % Kink Energy Field Strength \n")
            file_out.write("characteristicLength = 1; % [nm] \n")
            file_out.write("lsection = " + str(self.section) + "; \n")
            file_out.write("lcross = " + str(self.overlap) + "; \n")
            file_out.write("idxInvert = " + str(self.invIdx) + "; \n")
            file_out.write("offset = " + str(self.offset) + "; \n")
            file_out.write("pitch = " + str(self.cellSpacing + 1) + "; \n")
            file_out.write("radiusOfEffect = " + str(self.radiusOfEffect) + "; \n")
            file_out.write("numOfPeriods = " + str(self.numOfPeriods) + "; \n")
            file_out.write("clockSignalPeriod = " + str(self.clockPeriod) + "; \n")
            file_out.write("clockSignalAmp = " + str(self.clockAmp) + "; \n")
            file_out.write("clockSignalWavelength = " + str(self.clockWL) + "; \n")
            file_out.write("inputSignalType = '" + self.inputSignalType + "'; \n")
            file_out.write("inputSignalWavelength = " + str(self.inputWL) + "; \n")
            file_out.write("inputSignalAmp = " + str(self.inputAmp) + "; \n")
            file_out.write("inputSignalPeriod = clockSignalPeriod * 2; \n")
            file_out.write("inputSignalSharpness = " + str(self.inputShrp) + "; \n")
            file_out.write("inputSignalPhase = " + str(self.inputPhs) + "; \n")
            file_out.write("inputSignalMean = inputSignalAmp / 2; \n\n")

        with open(circuit) as file_in:
            with open(self.path + '/' + 'calculation.m', 'a+') as file_out:
                for line in file_in:
                    file_out.write(line)

        with open(signal) as file_in:
            with open(self.path + '/' + 'calculation.m', 'a+') as file_out:
                for line in file_in:
                    file_out.write(line)

        with open(naming) as file_in:
            with open(self.path + '/' + 'calculation.m', 'a+') as file_out:
                for line in file_in:
                    file_out.write(line)

        with open(workload) as file_in:
            with open(self.path + '/' + 'calculation.m', 'a+') as file_out:
                for line in file_in:
                    file_out.write(line)

    def makeBashFile(self):
        with open("calculation/submission.txt") as file_in:
            with open(self.path + '/' + 'calculation.sh', 'w+') as file_out:
                for line in file_in:
                    file_out.write(line)
