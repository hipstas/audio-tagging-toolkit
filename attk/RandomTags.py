#!/usr/bin/python

import os
import sys, getopt
import csv
import random
from pydub import AudioSegment
import time, datetime
import pandas as pd
import numpy as np
import subprocess
from time import gmtime, strftime



class RandomTags:
    """
    RandomTags
    """

    def __init__(self):
        self.temp=0




def media_duration(media_path):
    proc = subprocess.Popen(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',media_path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    duration = float(proc.stdout.read().strip())
    return duration


def random_tag(inputfile, script_path, out_dir, tag_secs=-1, n_clips=-1, per_duration=-1, extract=False):
    wav_source=True
    try:
        duration=media_duration(inputfile)-1.0   # Keeping clear of the last second to avoid common errors down the road
    except:
        print "ERROR: "+media_path
        return None
    if per_duration>0:
       n_clips=n_clips*int(round(duration/per_duration))
    start_times=[]
    counter=0
    while len(start_times) < int(n_clips):
        rand_time = round(random.random()*(duration-tag_secs),2)
        accepted=True
        for time in start_times:
            if rand_time < time < (rand_time + tag_secs):  ## Checking for overlap
                accepted=False
            if time < rand_time < (time + tag_secs):  ## Checking for overlap
                accepted=False
        if accepted==True:
            start_times.append(rand_time)
        counter+=1
        if counter > 1000000:
            print "*** Infinite loop error on: "+inputfile
            break
        return [(start,round(start+tag_secs,2)) for start in sorted(start_times)]  # list of 2-tuples: start and end times for random clips


#python ExcerptClass.py -i /path/to/audio.mp3 -t /path/to/tags.csv -e 1 -o /path/to/output/directory


def tags_to_csv(outputfile,tag_table,class_num=0,class_label=''):
    with open(outputfile, 'w') as csv_fo:
        csv_writer = csv.writer(csv_fo)
        for start, end in tag_table:
            if class_label=='':
                csv_writer.writerow([start,class_num,end])
            else:
                csv_writer.writerow([start,class_num,end,class_label])
        if len(tag_table)>0:
            csv_fo.write('\n\n## RandomTags.py run by '+str(os.getlogin()))
            csv_fo.write('\n## '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+' GMT\n')

def tags_to_wav(inputfile,basename,out_dir,tag_table):
    wav_source=True
    if inputfile.lower()[-4:]=='.mp4':     # Creates a temporary WAV
        wav_source=False                         # if input is MP4
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        audio_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, audio_path]) # '-y' option overwrites existing file if present
    else:
        audio_path=inputfile
    try:
        if audio_path[-4:].lower()=='.mp3':
            song = AudioSegment.from_mp3(audio_path)
        else:
            song = AudioSegment.from_wav(audio_path)
    except:
        print("Error loading audio with pyDub.")
        return("Error loading audio with pyDub.")
    for pair in tag_table:
        start = pair[0]
        duration = pair[1]-pair[0]
        clip_pathname=os.path.join(out_dir,basename+"_start_"+str(start)+"_dur_"+str(duration)+".wav")
        start_msec = float(start) * 1000.0
        duration_msec = float(duration) * 1000
        if not os.path.exists(clip_pathname):
            clip_data = song[start_msec:start_msec+duration_msec]
            clip_data=clip_data.set_channels(1)
            clip_data.export(clip_pathname, format="wav")






def main(argv):
    inputfile = ''
    extract=False
    class_id = 0
    out_dir=''
    tag_secs=3
    n_clips=1
    per_duration=-1
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hi:s:n:p:o:e",["ifile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--secs"): # tag length in seconds
            tag_secs = float(arg)
        elif opt in ("-n", "--num"): # tag length in seconds
            n_clips = int(arg)
        elif opt in ("-p", "--per"):
            per_duration = float(arg)
        elif opt in ("-o", "--out"):
            out_dir=arg
        if '-e' in sys.argv[1:]:
            extract=True
    basename=os.path.splitext(os.path.basename(inputfile))[0]
    filename=basename+"|%ss_x%sec_random.csv"%(str(tag_secs),str(n_clips))
    if per_duration > 0:
        filename=basename+"|%ssec_x%s_per_%ssec_random.csv"%(str(tag_secs),str(n_clips),str(per_duration))
    tag_table=random_tag(inputfile, script_path, out_dir, tag_secs, n_clips, per_duration, extract=False)
    if extract==True:
        tags_to_wav(inputfile,basename,out_dir,tag_table)
    else:
        tags_to_csv(os.path.join(out_dir,filename),tag_table,class_num=0,class_label='')



if __name__ == "__main__":
   main(sys.argv)
