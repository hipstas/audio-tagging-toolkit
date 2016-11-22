#!/usr/bin/python

import os
import sys, getopt
from pydub import AudioSegment
import time, datetime
import pandas as pd
import numpy as np





# Tying it all together

## Passed a row of tag metadata, this function extracts the corresponding audio and writes
## a WAV file.




def create_tag_excerpt(row):
    try:
        song = AudioSegment.from_wav(row['Pathname'])
    except:
        print "ERROR: "+row['Pathname']+" can't be found."
    start = row['Start']
    duration = row['Duration']
    start_msec = start * 1000.0
    duration_msec = duration * 1000
    clip_data = song[start_msec:start_msec+duration_msec]
    clip_pathname="Excerpt_"+row['Pathname'][:-4]+"_start_"+str(start)+"_dur_"+str(duration)+'_class_'+str(row['Class'])+'.wav'
    clip_data=clip_data.set_channels(1)
    clip_data.export(clip_pathname, format="wav", parameters=["-ar 44100", "-acodec pcm_s16le"])






def main(argv):
    inputfile = ''
    outputfile = ''
    excerpt_class = 1
    media_path=''
    try:
        opts, args = getopt.getopt(argv,"hi:m:o:e:v:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "'"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-e", "--excerptclass"):
            excerpt_class = int(arg)
        elif opt in ("-m", "--media"):
            media_path=arg

    tag_data = pd.read_csv(inputfile,header=None)
    if len(tag_data.iloc[0])==3:
        tag_data.columns=["Start","Class","Duration"]
    elif len(tag_data.iloc[0])==4:
        tag_data.columns=["Start","Class","Duration","Value"]
    tag_data['Pathname']=media_path
    
    tag_data_relevant=tag_data[tag_data['Class']==excerpt_class]
    
    for i in range(len(tag_data_relevant)):
        create_tag_excerpt(tag_data_relevant.iloc[i])
    


if __name__ == "__main__":
   main(sys.argv[1:])





