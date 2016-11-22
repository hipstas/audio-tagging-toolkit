#!/usr/bin/python

import sys, getopt
import os
import subprocess
import csv
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
    ranges=[(i,(x+1)-i) for i,x in ranges]       # Adding 1 to make time range inclusive. Format: (start_time,duration) 
    return ranges


def find_applause(inputfile,outputfile,plot):
    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=media_path.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile
	if outputfile=='':
		outputfile=inputfile[:-4]+'_applause.csv'
    classifier_model_path = './svm_applause_model'
    output, classesAll, acc, CM = aS.mtFileClassification(wav_path, classifier_model_path, "svm")
    output = list(output)
    applause_secs=[]
    for i, x in enumerate(output):
        if float(x)==1.0:
            applause_secs.append(i)
    applause_ranges=seconds_list_to_ranges(applause_secs)
    if (plot==True)&(len(applause_ranges)>0):
        print applause_ranges
        print '\n'
        pd.Series(output).plot()
        plt.show()
    if wav_source==False:
        os.remove(wav_path)
    with open(outputfile, 'w') as csv_fo:
		csv_writer = csv.writer(csv_fo)
		csv_writer.writerows(applause_ranges)


def main(argv):
    inputfile = ''
    outputfile = ''
    plot=False
    default_speaker=''
    try:
      opts, args = getopt.getopt(argv,"hi:o:pd:",["ifile=","ofile="])
    except getopt.GetoptError:
      print "FindApplause.py -i <inputfile> -o <outputfile> -p -d 'Default Speaker Name'"
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print "FindApplause.py -i <inputfile> -o <outputfile> -p -n 'Speaker Name'"
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif ("-p" in args):
          plot=True
      elif opt in ("-d"):
         default_speaker=arg
                  
    print inputfile
    print outputfile
    print plot
    print default_speaker

    if ('.mp3' in inputfile.lower())|('.wav' in inputfile.lower())|('.mp4' in inputfile.lower()):
        if (default_speaker!=''):
            find_applause_else_speaker(inputfile,outputfile,plot)
        else:
            find_applause(inputfile,outputfile,plot)



if __name__ == "__main__":
   main(sys.argv[1:])







