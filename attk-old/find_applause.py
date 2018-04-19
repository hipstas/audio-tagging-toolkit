#!/usr/bin/python

import sys, getopt
import os
import subprocess
import csv
import array
import random
from pyAudioAnalysis import audioSegmentation as aS
from itertools import groupby
from operator import itemgetter
from pydub import AudioSegment
from pydub.utils import get_array_type
from time import gmtime, strftime


here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)



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


def find_applause(inputfile,outputfile,to_csv,plot,default_speaker,buffer_secs,script_path):
    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile
    classifier_model_path = os.path.join(script_path,'data/svm_applause_model')
    output, classesAll, acc, CM = aS.mtFileClassification(wav_path, classifier_model_path, "svm")
    output = list(output)
    applause_secs=[]
    for i, x in enumerate(output):
        if float(x)==1.0:
            applause_secs.append(i)
    applause_ranges=seconds_list_to_ranges(applause_secs)
    if (plot==True)&(len(applause_ranges)>0):
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        print applause_ranges
        print '\n'
        pd.Series(output).plot()
        plt.title(inputfile.split('/')[-1])
        plt.xlabel('Seconds')
        plt.ylabel('Applause Classification')
        plt.show()
    if wav_source==False:
        os.remove(wav_path)
    if to_csv==True:
        if outputfile=='':
            outputfile=inputfile[:-4]+'_applause.csv'
        if default_speaker=='':
            with open(outputfile, 'w') as csv_fo:
                applause_ranges_expanded=[(start+buffer_secs,0,duration-buffer_secs) for start,duration in applause_ranges]
                csv_writer = csv.writer(csv_fo)
                csv_writer.writerows(applause_ranges_expanded)
        else:
            with open(outputfile, 'w') as csv_fo:
                prev_end='0.0'
                csv_writer = csv.writer(csv_fo)
                for start,duration in applause_ranges:
                    if float(float(start)-float(prev_end)-(float(buffer_secs)*2))>0.0:
                        csv_writer.writerow([float(prev_end)+buffer_secs,1,float(start)-float(prev_end)-(float(buffer_secs)*2),default_speaker.replace(',',';')])
                    if float(float(duration)-buffer_secs)>0:
                        csv_writer.writerow([start+buffer_secs,0,float(duration)-buffer_secs,'Applause'])
                    prev_end=start+duration
                if (prev_end < len(output)):
                    if float(float(len(output)-prev_end)-buffer_secs-1)>0.0:
                        csv_writer.writerow([float(prev_end)+buffer_secs,1,float(len(output)-prev_end)-buffer_secs-1,default_speaker.replace(',',';')]) # "-1" is a kluge to make sure final tag doesn't exceed length of audio file



def main(argv):
    inputfile = ''
    outputfile = ''
    plot=False
    default_speaker=''
    to_csv=False
    buffer_secs=1
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:pl:cb:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "FindApplause.py -i <inputfile> -o <outputfile> -p -l 'Default label'"
        sys.exit(2)
    if ("-b" in sys.argv[1:])|("--buffer" in sys.argv[1:]):
        buffer_secs=1
    for opt, arg in opts:
        if opt == '-h':
            print "FindApplause.py -i <inputfile> -o <outputfile> -p -n 'Speaker Name'"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg.strip('"')
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            to_csv=True
        elif opt in ("-l"):
            default_speaker=arg
        elif opt in ("-b"):
            buffer_secs=int(arg)
    if ("-p" in sys.argv[1:]):
        plot=True
    if ("-c" in sys.argv[1:])|("--csv" in sys.argv[1:]):
        to_csv=True
    if inputfile.lower()[-4:] in ('.wav','.mp3','.mp4'):
        find_applause(inputfile,outputfile,to_csv,plot,default_speaker,buffer_secs,script_path)
    elif os.path.isdir(sys.argv[-1]):
        media_dir=sys.argv[-1]
        media_paths=[os.path.join(media_dir,item) for item in os.listdir(media_dir)]
        counter=1
        for pathname in media_paths:
            if pathname.lower()[-4:] in ('.wav','.mp3','.mp4'):
                find_applause(pathname,outputfile,to_csv,plot,default_speaker,buffer_secs)
            print "****** "+str(counter)+" complete of "+str(len(media_paths))+" ******"




if __name__ == "__main__":
    main(sys.argv)
