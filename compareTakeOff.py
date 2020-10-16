import subprocess
import glob

strategies = ["Hungarian","Simplified"]
#groundFormations = ["Random","Linear","Circle","Regular matrix"]
#airFormations = ["Random","Linear","Circle","Regular matrix"]
groundFormations = ["Random","Linear"]
airFormations = ["Circle", "Regular matrix"]

protocolparametersFilePath = "compareTakeOff.properties"
ardusimParametersFilePath = "SimulationParam.properties"
logFilePath = "logFile.txt"

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
                cmd = ['java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath]
                try:
                    subprocess.run(cmd, timeout=5)
                except subprocess.TimeoutExpired:
                    with open(logFilePath, 'a') as file:
                        file.write(str(numUAVs) + ":" + strategy + ":" + ground + ":" + air + ":took to long\n")
                    directories_to_remove=glob.glob('virtual_uav_temp_*')
                    for directory in directories_to_remove:
                        cmd = ['rm','-r',directory]
                        subprocess.run(cmd)


print("simulation Done")

