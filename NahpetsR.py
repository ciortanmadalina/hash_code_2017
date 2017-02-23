numVids = 0
numRequestDesc = 0
cacheCount = 0
cacheSize = 0
endPointCaches = {}
endPointLatencies = {}
requestDescriptions = {}

class videoRequest:
    endPoint = -1
    videoID = -1
    requestCount = 0
    def __init__(self,a,b,c):
        endPoint = a
        videoID = b
        requestCount = c



def loadInputFile(fileName):
    f = open(fileName, 'r')

    line = f.readline()
    opts  =line.split(' ')

    numVids = int(opts[0])
    numEndPoints = int(opts[1])
    numRequestDesc = int(opts[2])
    cacheCount = int(opts[3])
    cacheSize = int(opts[4])

    #videos = []

    line = f.readline()
    videoSizes = line.split(' ')

    endPointLatencies = {}#[int(numEndPoints)]
    for endPointNum in range(numEndPoints):
        line = f.readline()
        opts = line.split(' ')
        endPointLatencies[endPointNum] = opts[0]
        endPointCaches[endPointNum] = {} #int(opts[1])]
        for curCacheNum in range(int(opts[1])):
            line = f.readline()
            lat = line.split(' ')
            endPointCaches[endPointNum][lat[0]] = lat[1]

    requestDescriptions = {}
    for requestNum in range(numRequestDesc):
        print(requestNum)
        line = f.readline()
        x = line.split(' ')

        vr = videoRequest(int(x[0]), int(x[1]), int(x[2]))

        requestDescriptions[vr.endPoint][vr.videoID] = vr





loadInputFile('short.in')



