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
from datetime import datetime
from time import gmtime, strftime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

working_dir = os.path.abspath('./')

#-i --infile
#-o --outfile (csv)
#-p --plot  / plot and print applause ranges to shell in hh:mm:ss format
#-n --name (default speaker for non-applause segments)

# Takes list of 0.2-second classifications
def class_list_to_time_rows(class_list,buffer_secs):
    try:
        prev_val=-1
        ranges=[]
        for i, x in enumerate(class_list):
            if x!=prev_val:
                ranges.append([i,int(x)])
            prev_val=x
        for i in range(len(ranges)):
            try: ranges[i].append(ranges[i+1][0])
            except: ranges[i].append(len(class_list))
        for triple in ranges:
            triple[0]=(triple[0]/5.0)+buffer_secs
            triple[2]=(triple[2]/5.0)-buffer_secs
        return ranges
    except:
        print "ERROR"



def diarize(inputfile,outputfile='',num_speakers=0,buffer_secs=0,to_csv=True,plot=False):
    if outputfile=='':
        outputfile=inputfile[:-4]+'.diarized.csv'
    try:
        wav_source=True
        if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
            wav_source=False                         # if input is MP3
            temp_filename=inputfile.split('/')[-1]+str(datetime.now()).replace(' ','__').replace(':','_')+'.wav'
            wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
            subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
        else:
            wav_path=inputfile
        os.chdir(here)
        print('Processing ...')
        output=aS.speakerDiarization(wav_path,numOfSpeakers=num_speakers,PLOT=plot)
        os.chdir(working_dir)
        output = list(output)
        class_rows=class_list_to_time_rows(output,buffer_secs)
        if wav_source==False:
            os.remove(wav_path)
        if to_csv==True:
            if outputfile=='':
                outputfile=inputfile[:-4]+'.diarized.csv'
            with open(outputfile, 'w') as csv_fo:
                csv_writer = csv.writer(csv_fo)
                csv_writer.writerows(class_rows)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def main(argv):
    inputfile = ''
    outputfile = ''
    plot=False
    to_csv=True
    buffer_secs=0
    num_speakers=0
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:pn:cb:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "FindApplause.py -i <inputfile> -o <outputfile> -p'"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "FindApplause.py -i <inputfile> -o <outputfile> -p"
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg.strip('"')
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            to_csv=True
        elif opt in ("-n","--num_speakers"):
            num_speakers = arg
        elif opt in ("-p","--plot"):
            plot=True
        elif opt ("-c","--csv"):
            to_csv=True
        elif opt ("-b","--buffer"):
            buffer_secs = arg
    if ('.mp3' in inputfile.lower())|('.wav' in inputfile.lower())|('.mp4' in inputfile.lower()):
        diarize(inputfile,outputfile,num_speakers,buffer_secs,to_csv,plot)
    elif os.path.isdir(sys.argv[-1]):
        media_dir=sys.argv[-1]
        media_paths=[os.path.join(media_dir,item) for item in os.listdir(media_dir)]
        for pathname in media_paths:
            if pathname.lower()[-4:] in ('.wav','.mp3','.mp4'):
                diarize(pathname,outputfile,num_speakers,buffer_secs,to_csv,plot)



if __name__ == "__main__":
   main(sys.argv)
