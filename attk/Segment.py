#!/usr/bin/python

import os
import sys, getopt
from pydub import AudioSegment
import time, datetime
import pandas as pd
import numpy as np
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)


def excerpt_segments(segments_df,inputfile,out_dir,mono):
    try:
        song = AudioSegment.from_wav(inputfile)
    except:
        return "ERROR: "+inputfile+" can't be found."
    start = float(segments_df[segments_df['Names']=="<START>"]['Instants'])
    end = float(segments_df[segments_df['Names']=="<END>"]['Instants'])
    start_msec = start * 1000.0
    end_msec = end * 1000
    clip_data = song[start_msec:end_msec]
    clip_pathname=out_dir+inputfile.split('/')[-1][:-4]+'_reading_excerpt'+'.wav'
    if mono==True:
        clip_data=clip_data.set_channels(1)
    clip_data.export(clip_pathname, format="wav", parameters=["-ar 48000", "-acodec pcm_s24le"])



def main(argv):
    inputfile = ''
    segments_path=''
    out_dir=''
    mono=False
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hi:s:o:m",["ifile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--segments"):
            segments_path=arg
        elif opt in ("-o", "--outdir"):
            out_dir=arg
    if '-m' in opts:
        mono=True

    segments_df = pd.read_csv(segments_path,header=None)
    segments_df.columns=["Instants","Names"]

    if out_dir=='':
        out_dir='/'.join(inputfile.split('/')[:-1])+'/'

    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile

    excerpt_segments(segments_df,inputfile,out_dir,mono)

    if wav_source==False:
        os.remove(wav_path)

if __name__ == "__main__":
   main(sys.argv)
