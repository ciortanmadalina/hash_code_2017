numVids = 0
numRequestDesc = 0
cacheCount = 0
cacheSize = 0
endPointCaches = {}
endPointLatencies = {}
requestDescriptions = {}
videosByCaches ={}
videoSizes =[]


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

    global numVids
    global numRequestDesc
    global cacheCount
    global cacheSize
    global endPointCaches
    global endPointLatencies
    global requestDescriptions
    global videosByCaches
    global videoSizes

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
            endPointCaches[endPointNum][lat[0]] = int(lat[1])

    requestDescriptions = {}
    for requestNum in range(numRequestDesc):
        print(requestNum)
        line = f.readline()
        x = line.split(' ')

        vr = videoRequest(int(x[0]), int(x[1]), int(x[2]))

        requestDescriptions[vr.endPoint] = vr




def loadVideosByCache1():
    for i in range (cacheCount):
        videosByCaches[i] = {}
        videosByCaches[i]['availableSpace'] = cacheSize
        videosByCaches[i]['videos'] = []

    for i in range (len(videoSizes)):
        videoSize = int(videoSizes[i])
        for cacheId  in videosByCaches:
            if videosByCaches[cacheId]['availableSpace'] >= videoSize :
                videosByCaches[cacheId]['videos'].append(i)
                videosByCaches[cacheId]['availableSpace'] -= videoSize
                break;


    print('videosByCaches end ', videosByCaches)






#loadInputFile('me_at_the_zoo.in')
#loadInputFile('kittens.in')

loadInputFile('short.in')
print('! video size', videoSizes)

print("endPointCaches :", endPointCaches)

loadVideosByCache1()



