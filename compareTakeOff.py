import subprocess

strategies = ["Hungarian","Simplified"]
#groundFormations = ["Random","Linear","Circle","Regular matrix"]
#airFormations = ["Random","Linear","Circle","Regular matrix"]
groundFormations = ["Random","Linear"]
airFormations = ["Circle", "Regular matrix"]

protocolparametersFilePath = "compareTakeOff.properties"
ardusimParametersFilePath = "SimulationParam.properties"

def writeProtocolParameters(strategy,ground,air,numUAVs):
    with open(protocolparametersFilePath, "w") as f:
        f.write("groundFormation=" + ground + "\n")
        f.write("numberOfClusters=3\n")
        f.write("groundMinDistance=10\n")
        f.write("takeOffStrategy=" + strategy + "\n")
        f.write("flyingFormation=" + air + "\n")
        f.write("flyingMinDistance=50\n")
        f.write("outputFile=compareTakeOff" + str(numUAVs) + ".csv")  

def writeArduSimParameters(numUAVs):
    with open(ardusimParametersFilePath,'r') as file:
        data = file.readlines()

    # replace the numbers of UAVS on line 3
    data[3] = "numUAVs=" + str(numUAVs) + "\n"
    with open(ardusimParametersFilePath,'w') as file:
        file.writelines(data)



for a in range(1,4):
    numUAVs = a*5
    writeArduSimParameters(numUAVs)
    for strategy in strategies:
        for ground in groundFormations:
            for air in airFormations:
                writeProtocolParameters(strategy,ground,air,numUAVs)
                subprocess.call(['java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath])

print("simulation Done")

