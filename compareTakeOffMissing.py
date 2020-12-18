import subprocess
import glob
import os.path

experiment = [["Hungarian","Random","Linear"],["Hungarian","Linear","Random"]]
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

def getTotalTime(filename):
    totalTime=0
    counter=0
    with open(filename, 'r') as file:
        allData = file.readlines()
    
    for data in allData:
        if data == "\n":
            continue

        values = data.split(";")
        time = values[-2]
        totalTime = totalTime + int(time)
        counter = counter +1
    avarage =  totalTime/counter
    return avarage/1000

def getEstimatedForTimeout(numUAVs):
    filename = "compareTakeOff" + str(numUAVs) + ".csv"
    if os.path.isfile(filename):
        return getTotalTime(filename)*2
    else:
        return 1800    

def removeFoldersAfterError():
    directories_to_remove=glob.glob('virtual_uav_temp_*')
    for directory in directories_to_remove:
        cmd = ['rm','-r',directory]
        subprocess.run(cmd)


numUAVs = 20
writeArduSimParameters(numUAVs)
for ex in experiment:
    writeProtocolParameters(ex[0],ex[1],ex[2],numUAVs)
    cmd = ['jdk-13/bin/java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath]
    try:
        time = getEstimatedForTimeout(numUAVs)
        subprocess.run(cmd, timeout=time)
    except subprocess.TimeoutExpired:
        removeFoldersAfterError()        
        cmd = ['jdk-13/bin/java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath]
        try:
       	    time = getEstimatedForTimeout(numUAVs)
            subprocess.run(cmd, timeout=time)
        except subprocess.TimeoutExpired:
            with open(logFilePath, 'a') as file:
                file.write(str(numUAVs) + ":" + ex[0]  + ":" + ex[1] + ":" + ex[2] + ":took to long\n")

print("simulation Done")
