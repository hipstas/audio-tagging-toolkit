#!/usr/bin/python

import os
import sys, getopt
from pydub import AudioSegment
import time, datetime
import pandas as pd
import numpy as np
import subprocess





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
    if len(row)==6:
        clip_pathname=row['Out Directory']+row['Basename']+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(row['Class'])+'.wav'
    elif len(row)>6:
        clip_pathname=row['Out Directory']+row['Basename']+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(row['Class'])+'_label_'+str(row['Label'])+'.wav'
    clip_data=clip_data.set_channels(1)
    clip_data.export(clip_pathname, format="wav", parameters=["-ar 44100", "-acodec pcm_s16le"])






def main(argv):
    inputfile = ''
    excerpt_class = 1
    tag_path=''
    out_dir=''
    try:
        opts, args = getopt.getopt(argv,"hi:t:e:o:",["ifile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-e", "--excerptclass"):
            excerpt_class = int(arg)
        elif opt in ("-t", "--tags"):
            tag_path=arg
        elif opt in ("-o", "--outdir"):
            out_dir=arg

    tag_data = pd.read_csv(tag_path,header=None)
    if len(tag_data.iloc[0])==3:
        tag_data.columns=["Start","Class","Duration"]
    elif len(tag_data.iloc[0])==4:
        tag_data.columns=["Start","Class","Duration","Label"]
        
    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile
    
    tag_data['Pathname']=wav_path
    if out_dir=='':
        tag_data['Out Directory']='/'.join(inputfile.split('/')[:-1])+'/'
    else:
        tag_data['Out Directory']=out_dir
    tag_data['Basename']=inputfile.split('/')[-1][:-4]
    
    tag_data_relevant=tag_data[tag_data['Class']==excerpt_class]

    for i in range(len(tag_data_relevant)):
        create_tag_excerpt(tag_data_relevant.iloc[i])

    if wav_source==False:
        os.remove(wav_path)

if __name__ == "__main__":
   main(sys.argv[1:])





