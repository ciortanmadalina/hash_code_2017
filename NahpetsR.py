

numVids = 0
numRequestDesc = 0
cacheCount = 0
cacheSize = 0
endpointCaches = []
endPointLatencies = []

def loadInputFile(fileName):
    f = open(fileName, 'r')

    line = f.readline()
    opts  =line.split(' ')

    numVids = opts[0]
    numEndPoints = opts[1]
    numRequestDesc = opts[2]
    cacheCount = opts[3]
    cacheSize = opts[4]

    videos = []

    line = f.readline()
    videoSizes = line.split(' ')

    for endPointNum in range(int(numEndPoints)):
        line = f.readline()
        opts = line.split(' ')
        endPointLatencies[endPointNum] = opts[0]
        endpointCaches[endPointNum] = []
        for curCacheNum in range(opts[1]):
            line = f.readline()
            #endPointCaches[endPointNum][]



loadInputFile('kittens.in')


