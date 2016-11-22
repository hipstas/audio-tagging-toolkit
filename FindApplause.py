#!/usr/bin/python

import sys, getopt
import os
import subprocess
import array
import random
import pandas as pd
import numpy as np
from pyAudioAnalysis import audioSegmentation as aS
from itertools import groupby
from operator import itemgetter
from pydub import AudioSegment
from pydub.utils import get_array_type
import matplotlib.pyplot as plt
from IPython.display import display, Audio

#-i --infile
#-o --outfile (csv) (if none, replace file extension with cab)
#-p --plot  / plot and print applause ranges to shell in hh:mm:ss format
#-n --name (default speaker for non-applause segments)



# Takes list of 1-second segments classified as applause (1.0) or 
# non-applause (0.0) and returns list of 2-tuples specifying applause ranges
def seconds_list_to_ranges(seconds_list): 
    ranges = []                
    for k, g in groupby(enumerate(seconds_list), lambda (i,x):i-x):
        group = map(itemgetter(1), g)
        ranges.append((group[0], group[-1]))
    ranges=[(i,x+1) for i,x in ranges]
    return ranges



def find_applause(audio_path,plot):
    is_mp3=False
    if audio_path.lower()([-4:]=='.mp3')|([-4:]=='.mp4'):     # Creates a temporary WAV
        is_mp3=True                         # if input is MP3
        random.seed(audio_path)
        wav_path='/var/tmp/'+str(random.random())+'_temp.wav'   # Filename for temp WAV is random number
        subprocess.call(['ffmpeg', '-y', '-i', audio_path, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=audio_path
    classifier_model_path = 'svm_applause_model'
    output, classesAll, acc, CM = aS.mtFileClassification(wav_path, classifier_model_path, "svm")
    output = list(output)
    counter=0
    applause_secs=[]
    for value in output:
        if float(value)==1.0:
            applause_secs.append(counter)
        counter+=1
    applause_ranges=seconds_list_to_ranges(applause_secs)
    if len(applause_ranges)>0:
        print "Applause segments at 1-second resolution."
        if plot==True:
            print applause_ranges
            print '\n'
            pd.Series(output).plot()
            plt.show()
    if is_mp3==True:
        os.remove(wav_path)



# Classifies audio at 1-second resolution, plots results if applause found, 
# and returns applause ranges as list of 2-tuples.
# Add 1 to 2nd value in each 2-tuple for inclusive time span.
def find_applause(audio_path,plot):
    is_mp3=False
    if (audio_path.lower()[-4:]=='.mp3')|(audio_path.lower()[-4:]=='.mp4'):    # Creates a temporary WAV
        is_mp3=True                        # if input is MP3
        random.seed(audio_path)
        wav_path='/var/tmp/'+str(random.random())+'_temp.wav' # Filename for temp WAV is a random float
        subprocess.call(['ffmpeg', '-y', '-i', audio_path, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=audio_path
    classifier_model_path = "svm_applause_model" 
    output, classesAll, acc, CM = aS.mtFileClassification(wav_path, classifier_model_path, "svm")
    output = list(output)
    counter=0
    applause_secs=[]
    for value in output:
        if value>0.0:
            applause_secs.append(counter)
        counter+=1
    applause_ranges=seconds_list_to_ranges(applause_secs)
    if len(applause_ranges)>0:
        print applause_ranges
        print '\n'
        #pd.Series(output).plot()
        #plt.show()
    #for pair in applause_ranges:
        #print pair
        #display_clip(wav_path,pair[0],pair[1]+1)     ## show audio clips
    if is_mp3==True:
        os.remove(wav_path)
    print audio_path
    for pair in applause_ranges:
        print "%s,2,%s,Applause"%(str(pair[0]),str(pair[1]+1))
    with open(audio_path[:-4]+'.csv','w') as fo:
        for pair in applause_ranges:
            fo.write("%s,0,%s,Applause"%(str(float(pair[0])),str(float(pair[1]+1))))
            fo.write('\n')
    return applause_ranges




def find_applause_else_speaker(audio_path,speaker_name,plot):
    is_mp3=False
    if (audio_path.lower()[-4:]=='.mp3')|(audio_path.lower()[-4:]=='.mp4'):    # Creates a temporary WAV
        is_mp3=True                        # if input is MP3
        random.seed(audio_path)
        wav_path='/var/tmp/'+str(random.random())+'_temp.wav' # Filename for temp WAV is a random float
        subprocess.call(['ffmpeg', '-y', '-i', audio_path, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=audio_path
    classifier_model_path = "/Users/mclaugh/Dropbox/WGBH_ARLO_Project/audio-ml-demo-code/Applause_Classifier/svm_applause" # Or replace with sklearn model pathname
    output, classesAll, acc, CM = aS.mtFileClassification(wav_path, classifier_model_path, "svm")
    output = list(output)
    counter=0
    applause_secs=[]
    for value in output:
        if value>0.0:
            applause_secs.append(counter)
        counter+=1
    applause_ranges=seconds_list_to_ranges(applause_secs)
    if len(applause_ranges)>0:
        print applause_ranges
        print '\n'
        #pd.Series(output).plot()
        #plt.show()
    #for pair in applause_ranges:
        #print pair
        #display_clip(wav_path,pair[0],pair[1]+1)     ## show audio clips
    if is_mp3==True:
        os.remove(wav_path)
    print audio_path
    for pair in applause_ranges:
        print "%s,2,%s,Applause"%(str(pair[0]),str(pair[1]+1))
    with open(audio_path[:-4]+'.csv','w') as fo:
        prev_end='0.0'
        for pair in applause_ranges:
            fo.write("%s,1,%s,%s\n"%(str(prev_end),str(float(pair[0])),speaker_name.replace(',',';')))
            fo.write("%s,0,%s,Applause\n"%(str(float(pair[0])),str(float(pair[1]+1))))
            prev_end=float(pair[1]+1)
    return applause_ranges



def main(argv):
    inputfile = ''
    outputfile = ''
    plot=False
    default_speaker=''
    try:
      opts, args = getopt.getopt(argv,"hi:o:pn:",["ifile=","ofile="])
    except getopt.GetoptError:
      print "FindApplause.py -i <inputfile> -o <outputfile> -p -n 'Speaker Name'"
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print "FindApplause.py -i <inputfile> -o <outputfile> -p -n 'Speaker Name'"
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-p"):
          plot=True
      elif opt in ("-n"):
         default_speaker=arg
                  
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    if ('.mp3' in inputfile.lower())|('.wav' in inputfile.lower())|('.mp4' in inputfile.lower()):
        if (default_speaker!=''):
            
        else:
            find_applause(inputfile,plot)



if __name__ == "__main__":
   main(sys.argv[1:])







