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


#-i --infile
#-o --outfile (csv) (if none, replace file extension with cab)
#-p --plot  / plot and print applause ranges to shell in hh:mm:ss format
#-n --name (default speaker for non-applause segments)


# Takes list of 0.2-second classifications
def class_list_to_time_rows(class_list):
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
        triple[0]=triple[0]/5.0
        triple[2]=triple[2]/5.0
    return ranges




def find_applause(inputfile,outputfile,to_csv,plot,numSpeakers,buffer_secs):
    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile
    output=aS.speakerDiarization(wav_path,numOfSpeakers=numSpeakers,PLOT=plot)
    output = list(output)
    class_rows=class_list_to_time_rows(class_list)
    if wav_source==False:
        os.remove(wav_path)
    if to_csv==True:
        with open(outputfile, 'w') as csv_fo:
            csv_writer = csv.writer(csv_fo)
            csv_writer.writerows(class_rows)
            # for start,duration in applause_ranges:
#                 if float(float(start)-float(prev_end)-(float(buffer_secs)*2))>0.0:
#                     csv_writer.writerow([float(prev_end)+buffer_secs,1,float(start)-float(prev_end)-(float(buffer_secs)*2),default_speaker.replace(',',';')])
#                 if float(float(duration)-buffer_secs)>0:
#                     csv_writer.writerow([start+buffer_secs,0,float(duration)-buffer_secs,'Applause'])
#                 prev_end=start+duration
                #print prev_end
                #print len(output)
            #if (prev_end < len(output)):
                #if float(float(len(output)-prev_end)-buffer_secs-1)>0.0:
                    #csv_writer.writerow([float(prev_end)+buffer_secs,1,float(len(output)-prev_end)-buffer_secs-1,default_speaker.replace(',',';')]) # "-1" is a kluge to make sure final tag doesn't exceed length of audio file



def main(argv):
    inputfile = ''
    outputfile = ''
    plot=False
    to_csv=False
    buffer_secs=0
    numSpeakers=0
    try:
        opts, args = getopt.getopt(argv,"hi:o:pn:cb",["ifile=","ofile="])
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
        elif opt in ("-n"):
            numSpeakers=arg
    if ("-p" in sys.argv[1:]):
        plot=True
    if ("-c" in sys.argv[1:])|("--csv" in sys.argv[1:]):
        to_csv=True
    if ("-b" in sys.argv[1:])|("--buffer" in sys.argv[1:]):
        buffer_secs=1
    if ('.mp3' in inputfile.lower())|('.wav' in inputfile.lower())|('.mp4' in inputfile.lower()):
        find_applause(inputfile,outputfile,to_csv,plot,default_speaker,buffer_secs)





if __name__ == "__main__":
   main(sys.argv[1:])







