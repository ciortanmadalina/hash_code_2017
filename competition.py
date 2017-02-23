import NahpetsR

print('test')
print('blah')
print('qsdqsd')

NahpetsR.petitchat()


class endPointVolume:
    endpoint = -1
    video = -1
    requests = 0
    volume = 0

requestDescriptions = {}
videoSizes = {}

endPointVolumes = []

def assignByEndpointVolume():
    for endpidx in len(requestDescriptions):
        vr = requestDescriptions[endpidx]
        videoVolume = videoSizes[vr.videoID] * vr.requestCount

        epv = endPointVolume()
        epv.endpoint = vr.endPoint
        epv.video = vr.videoID
        epv.requests = vr.requestCount
        epv.volume = videoVolume

        endPointVolumes.append(epv)

    # now sort by endPointVolume

    sorted(endPointVolumes, key=)


