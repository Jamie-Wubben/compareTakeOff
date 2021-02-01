import subprocess
import glob
import os.path

strategies = ["Hungarian","Simplified"]
groundFormations = ["Random"]
airFormations = ["Regular matrix","Circle","Linear"]

protocolparametersFilePath = "compareTakeOff.properties"
ardusimParametersFilePath = "SimulationParam.properties"
logFilePath = "logFile.txt"
sequential = "false"

def writeProtocolParameters(strategy,ground,air,numUAVs):
    with open(protocolparametersFilePath, "w") as f:
        f.write("groundFormation=" + ground + "\n")
        f.write("numberOfClusters=3\n")
        f.write("groundMinDistance=10\n")
        f.write("takeOffStrategy=" + strategy + "\n")
        f.write("flyingFormation=" + air + "\n")
        f.write("flyingMinDistance=50\n")
        f.write("outputFile=randomToMatrix.csv\n")
        f.write("takeOffIsSequential=" + str(sequential) + "\n")
        f.write("altitude=10")  

def writeArduSimParameters(numUAVs):
    with open(ardusimParametersFilePath,'r') as file:
        data = file.readlines()

    # replace the numbers of UAVS on line 3
    data[3] = "numUAVs=" + str(numUAVs) + "\n"
    with open(ardusimParametersFilePath,'w') as file:
        file.writelines(data)

def removeFoldersAfterError():
    directories_to_remove=glob.glob('virtual_uav_temp_*')
    for directory in directories_to_remove:
        cmd = ['rm','-r',directory]
        subprocess.run(cmd)

for ground in groundFormations:
    for strategy in strategies:
        for air in airFormations:
            for a in range(1,9):
                numUAVs = a*25
                writeArduSimParameters(numUAVs)
                writeProtocolParameters(strategy,ground,air,numUAVs)
                cmd = ['jdk-13/bin/java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath]
                try:
                    print("running " + str(numUAVs) + " drones going to " + air + " with " + strategy)
                    subprocess.run(cmd, timeout=600)
                    with open(logFilePath, 'a') as file:
                        file.write(str(numUAVs) + ";" + strategy + ";" + ground + ";" + air + ";executed correctly\n")
                except subprocess.TimeoutExpired:
                    removeFoldersAfterError()
                    with open(logFilePath, 'a') as file:
                        file.write(str(numUAVs) + ";" + strategy  + ";" + ground  + ";" + air + ";took to long\n")

print("simulation Done")

