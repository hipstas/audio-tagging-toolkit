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


here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

def media_duration(media_path):
    proc = subprocess.Popen(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',media_path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    duration = float(proc.stdout.read().strip())
    return duration


def random_tag(media_path, out_dir, clip_secs=-1, num_tags=1, per_duration=-1, extract=False):
    wav_source=True
    try:
        duration=media_duration(media_path)-1.0   # Keeping clear of the last second to avoid common errors down the road
    except:
        print "ERROR: "+media_path
        return None
    if not per_duration>0:
        per_duration =  duration
    num_tags=num_tags*int(round(duration/per_duration))
    start_times=[]
    counter=0
    while len(start_times) < int(num_tags):
        rand_time = round(random.random()*(duration-clip_secs),2)
        accepted=True
        for time in start_times:
            if rand_time < time < (rand_time + clip_secs):  ## Checking for overlap
                accepted=False
            if time < rand_time < (time + clip_secs):  ## Checking for overlap
                accepted=False
        if accepted==True:
            start_times.append(rand_time)
        counter+=1
        if counter > 1000000:
            print "*** Infinite loop error on: "+media_path
            break
    tag_pairs = [(start,round(start+clip_secs,2)) for start in sorted(start_times)]
    if extract==True:
        tags_to_wav(media_path,out_dir,tag_pairs)
    return tag_pairs  # list of 2-tuples: start and end times for random clips


#python ExcerptClass.py -i /path/to/audio.mp3 -t /path/to/tags.csv -e 1 -o /path/to/output/directory


def tags_to_csv(csv_filename,tag_pairs,class_num=0,class_label=''):
    with open(csv_filename, 'w') as csv_fo:
        csv_writer = csv.writer(csv_fo)
        for start, end in tag_pairs:
            if class_label=='':
                csv_writer.writerow([start,class_num,end])
            else:
                csv_writer.writerow([start,class_num,end,class_label])
        if len(tag_pairs)>0:
            csv_fo.write('\n\n## RandomTags.py run by '+str(os.getlogin()))
            csv_fo.write('\n## '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+' GMT\n')

def tags_to_wav(media_path,out_dir,tag_pairs):
    basename=os.path.splitext(os.path.basename(media_path))[0]
    wav_source=True
    if media_path.lower()[-4:] not in ('.mp3','.wav'):     # Creates a temporary WAV
        wav_source=False                         # if input is MP4
        temp_filename=media_path.split('/')[-1]+'_temp.wav'
        audio_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', media_path, audio_path]) # '-y' option overwrites existing file if present
    else:
        audio_path=media_path
    try:
        if audio_path[-4:].lower()=='.mp3':
            song = AudioSegment.from_mp3(audio_path)
        else:
            song = AudioSegment.from_wav(audio_path)

    except Exception as inst:
        print(inst)
        sys.exit(2)

    for pair in tag_pairs:
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
    media_path = ''
    extract=False
    class_id = 0
    out_dir=''
    clip_secs=3
    num_tags=1
    per_duration=-1
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hei:s:n:p:o:",["ifile=","secs=","num=","per=","out="])
    except Exception as inst:
        print(inst)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            media_path = arg
        elif opt in ("-s", "--secs"): # tag length in seconds
            clip_secs = float(arg)
        elif opt in ("-n", "--num"): # tag length in seconds
            num_tags = int(arg)
        elif opt in ("-p", "--per"):
            per_duration = float(arg)
        elif opt in ("-o", "--out"):
            out_dir=arg
        elif opt in ("-e", "--extract"):
            extract=True
    tag_pairs=randomtag(media_path, out_dir, clip_secs, num_tags, per_duration, extract=False)
    if extract==True:
        tags_to_wav(media_path,out_dir,tag_pairs)
    else:
        basename=os.path.splitext(os.path.basename(media_path))[0]
        csv_filename=basename+"|%ss_x%sec_random.csv"%(str(clip_secs),str(num_tags))
        if per_duration > 0:
            csv_filename=basename+"|%ssec_x%s_per_%ssec_random.csv"%(str(clip_secs),str(num_tags),str(per_duration))
        tags_to_csv(os.path.join(out_dir,csv_filename),tag_pairs,class_num=0,class_label='')



if __name__ == "__main__":
   main(sys.argv)
