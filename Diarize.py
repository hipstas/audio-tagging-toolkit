#!/usr/bin/python

from pyAudioAnalysis import audioSegmentation as aS

def speakerDiarizationWrapper(inputFile, numSpeakers, useLDA):
    if useLDA:
        aS.speakerDiarization(inputFile, numSpeakers, PLOT=True)
    else:
        aS.speakerDiarization(inputFile, numSpeakers, LDAdim=0, PLOT=False)

numSpeakers=2
wav_path="/Users/mclaugh/Dropbox/WGBH_ARLO_Project/Extended_Corpus/Clinton/Clinton_mp4s/cpb-aacip-189-12m6402b.h264.wav"

import os
os.chdir('/Users/mclaugh/Dropbox/WGBH_ARLO_Project/pyAudioAnalysis/')

dd=aS.speakerDiarization(wav_path,numOfSpeakers=numSpeakers,PLOT=False)



#-i --infile
#-o --outfile (csv)
#-n number of speakers
