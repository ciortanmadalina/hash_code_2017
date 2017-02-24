import operator

numVids = 0
numVids = 0
numRequestDesc = 0
cacheCount = 0
cacheSize = 0
endPointCacheLantencies = {}
endPointDatacenterLatencies = {}
requestDescriptions = {}
videosByCaches ={}
videoSizes =[]


class endPointVolume:
    endpoint = 0
    video = 0
    requests = 0
    volume = 0

def initVars():
    global numVids
    global numRequestDesc
    global cacheCount
    global cacheSize
    global endPointCacheLantencies
    global endPointDatacenterLatencies
    global requestDescriptions
    global videosByCaches
    global videoSizes

    numVids = 0
    numVids = 0
    numRequestDesc = 0
    cacheCount = 0
    cacheSize = 0
    endPointCacheLantencies = {}
    endPointDatacenterLatencies = {}
    requestDescriptions = {}
    videosByCaches ={}
    videoSizes =[]


def assignByEndpointVolume():
    endpointVolumes = []
    global numVids
    global numRequestDesc
    global cacheCount
    global cacheSize
    global endPointCacheLantencies
    global endPointDatacenterLatencies
    global requestDescriptions
    global videosByCaches
    global videoSizes

    for endpidx in requestDescriptions:

        for videoID in requestDescriptions[endpidx]:
            vr = requestDescriptions[endpidx][videoID]
            videoVolume = int(videoSizes[vr.videoID]) * vr.requestCount

            epv = endPointVolume()
            epv.endpoint = vr.endPoint
            epv.video = vr.videoID
            epv.requests = vr.requestCount
            epv.volume = videoVolume

            endpointVolumes.append(epv)

    # now sort by endPointVolume

    endpointVolumes = sorted(endpointVolumes, key=lambda epv:epv.volume, reverse=True)

    #print(endpointVolumes)
    # this is a list of request count * file size, per endpoint
    # assign each video to the best cache, if one is available, assuming the video isn't already present in the best one

    for i in range (cacheCount):
        videosByCaches[i] = {}
        videosByCaches[i]['availableSpace'] = cacheSize
        videosByCaches[i]['videos'] = []

    for epv in endpointVolumes:
        videoSize = int(videoSizes[epv.video])
        #try to stick the video in the best available cache

        sortedLatencyCacheIndex = sorted(endPointCacheLantencies[epv.endpoint].keys(), key=lambda epclkey:endPointCacheLantencies[epv.endpoint][epclkey]  )



        for cacheID in sortedLatencyCacheIndex:
            if ( epv.video in videosByCaches[int(cacheID)]['videos'] ):
                break; # don't put the video if it's already in there ;-)
            if videosByCaches[int(cacheID)]['availableSpace'] >= videoSize:
                # found a place to put the video, maybe check if it's already not too far

                videosByCaches[int(cacheID)]['videos'].append(epv.video)
                videosByCaches[int(cacheID)]['availableSpace'] -= videoSize
                break;




class videoRequest:
    endPoint = -1
    videoID = -1
    requestCount = 0
    def __init__(self,a,b,c):
        self.endPoint = b
        self.videoID = a
        self.requestCount = c



def loadInputFile(fileName):
    f = open(fileName, 'r')

    global numVids
    global numRequestDesc
    global cacheCount
    global cacheSize
    global endPointCacheLantencies
    global endPointDatacenterLatencies
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


    endPointDatacenterLatencies = {}#[int(numEndPoints)]
    for endPointNum in range(numEndPoints):
        line = f.readline()
        opts = line.split(' ')
        endPointDatacenterLatencies[endPointNum] = opts[0]
        endPointCacheLantencies[int(endPointNum)] = {} #int(opts[1])]
        for curCacheNum in range(int(opts[1])):
            line = f.readline()
            lat = line.split(' ')
            endPointCacheLantencies[int(endPointNum)][lat[0]] = int(lat[1])

    requestDescriptions = {}
    for requestNum in range(numRequestDesc):
        #print(requestNum)
        line = f.readline()
        x = line.split(' ')

        vr = videoRequest(int(x[0]), int(x[1]), int(x[2]))

        if ( vr.endPoint not in requestDescriptions):
            requestDescriptions[vr.endPoint] = {}

        requestDescriptions[vr.endPoint][vr.videoID] = vr




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


    #print('videosByCaches end ', videosByCaches)



def writeToFile(score, videosByCaches, fileName) :
    cachesUsed = 0
    for cacheId in videosByCaches:
        if len(videosByCaches[cacheId]['videos']) > 0 :
            cachesUsed += 1

    outputFile = open(fileName + '.out', 'w')
    outputFile.write(str(cachesUsed))
    outputFile.write("\n")
    for cacheId in videosByCaches:
        if len(videosByCaches[cacheId]['videos']) > 0 :
            outputFile.write(str(cacheId))
            outputFile.write(' ')
            outputFile.write(' '.join(map( str, videosByCaches[cacheId]['videos'])))
            #outputFile.write(' '.join(videosByCaches[cacheId]['videos']))
            outputFile.write("\n")

    outputFile.close()


def score(fileName):
    global numVids
    global numRequestDesc
    global cacheCount
    global cacheSize
    global endPointCacheLantencies
    global endPointDatacenterLatencies
    global requestDescriptions
    global videosByCaches
    global videoSizes

    total = 0
    for endp in requestDescriptions:
        totalEP = 0
        for videoID in requestDescriptions[endp]:
            vr = requestDescriptions[endp][videoID]
            latDC = int(endPointDatacenterLatencies[endp])
            bestCacheLat = 0

            for cacheID in endPointCacheLantencies[endp]:
                if videoID in videosByCaches[int(cacheID)]["videos"]:
                    #print(endPointCacheLantencies[endp][cacheID])
                    if latDC - int(endPointCacheLantencies[endp][cacheID]) > bestCacheLat:
                        bestCacheLat = latDC - endPointCacheLantencies[endp][cacheID]

            if bestCacheLat < 0:
                bestCacheLat = 0 #if one cache server has worse latency than datacenter
            totalEP += vr.requestCount * bestCacheLat

        total += totalEP
        #print("temp total:" , total , " EP:" ,totalEP)
    print("done:" ,total)
    writeToFile(total, videosByCaches, fileName)






#loadInputFile('me_at_the_zoo.in') #17439038
#loadInputFile('kittens.in') # 535877848672
#loadInputFile('trending_today.in') #238174174000
#loadInputFile('videos_worth_spreading.in') #20626135655




#print("endPointCaches :", endPointCacheLantencies)

#loadVideosByCache1()
#score()

fileNames = ['me_at_the_zoo.in','videos_worth_spreading.in','trending_today.in','kittens.in']

for fileName in fileNames:
    initVars()
    loadInputFile(fileName)
    assignByEndpointVolume()
    score(fileName)

print("finished")

print(videosByCaches)