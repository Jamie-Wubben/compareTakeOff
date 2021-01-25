import subprocess
import glob
import os.path

strategies = ["Hungarian","Simplified"]
groundFormations = ["Random"]
airFormations = ["Regular matrix"]

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
        time = values[-2] #last item is a \n so -2 to get full time
        try:
            totalTime = totalTime + int(time)
            counter = counter +1
        except:
            pass
  
    if counter >0:    
        avarage = totalTime/counter
        return avarage/1000
    else:
        return 1500

def getEstimatedForTimeout(numUAVs):
    filename = "compareTakeOff" + str(numUAVs) + ".csv"
    if os.path.isfile(filename):
        return getTotalTime(filename)+180
    else:
        return 1500

def removeFoldersAfterError():
    directories_to_remove=glob.glob('virtual_uav_temp_*')
    for directory in directories_to_remove:
        cmd = ['rm','-r',directory]
        subprocess.run(cmd)

for a in range(1,8):
    numUAVs = a*25
    writeArduSimParameters(numUAVs)
    for strategy in strategies:
        for ground in groundFormations:
            for air in airFormations:
                writeProtocolParameters(strategy,ground,air,numUAVs)
                cmd = ['jdk-13/bin/java','-jar', 'ArduSim.jar', 'simulator-cli', ardusimParametersFilePath]
                try:
                    time = getEstimatedForTimeout(numUAVs)
                    if time <= 1500:
                        print("timeout is set to " + str(time) + " seconds")
                        subprocess.run(cmd, timeout=time)
                        with open(logFilePath, 'a') as file:
                            file.write(str(numUAVs) + ";" + strategy + ";" + ground + ";" + air + ";executed correctly\n")
                    else:
                        with open(logFilePath, 'a') as file:
                            file.write(str(numUAVs) + ";" + strategy + ";" + ground + ";" + air + ";estimated time is longer than battery cap\n") 
                except subprocess.TimeoutExpired:
                    removeFoldersAfterError()
                    with open(logFilePath, 'a') as file:
                        file.write(str(numUAVs) + ";" + strategy  + ";" + ground  + ";" + air + ";took to long\n")

print("simulation Done")

