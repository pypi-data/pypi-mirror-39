import os

def connect(leagueExecutablePath = None):
# Get riot games folder location here somehow
    if(leagueExecutablePath == None):
        path = "C:/Riot Games/League of Legends/lockfile"
    else:
        path = "zz"
    if(checkLockFile(path)):
        return createAddress(readLockFile(path))
    else:
        return "Ensure the client is running and you supplied the correct path"

def checkLockFile(path): 
    return os.path.exists(path)

def readLockFile(path):
    f = open(path, 'r')
    data = f.read()
    data = data.split(":")
    # data[0] == "LeagueClient"
    # data[1] == idk rn
    # data[2] == port number
    # data[3] == auth token
    # data[4] == connecton method
    return data

def createAddress(data):
    return "127.0.0.1:" + data[2]

    


