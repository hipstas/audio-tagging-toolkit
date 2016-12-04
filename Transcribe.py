#!/usr/bin/python

import sys, getopt
import os
import array
import random
import speech_recognition as sr
import subprocess


#-i --infile
#-o --outfile (csv) (if none, replace file extension with .csv)
#-t --txt Plain text output


def transcribe(inputfile,outputfile,to_txt):
    wav_source=True
    if inputfile.lower()[-4:]!='.wav':     # Creates a temporary WAV
        wav_source=False                         # if input is MP3
        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
        wav_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path]) # '-y' option overwrites existing file if present
    else:
        wav_path=inputfile
    transcript=''
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)    # read the entire audio file
    try:                           # recognize speech using Sphinx
        transcript=r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio.")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    if to_txt==True:
        if outputfile=='':
            outputfile=inputfile[:-4]+'_transcript.txt'
        with open(outputfile, 'w') as fo:
            fo.write(transcript)
    else:
        print transcript
    if wav_source==False:
        os.remove(wav_path)
     


def main(argv):
    inputfile = ''
    outputfile = ''
    to_txt=False
    try:
        opts, args = getopt.getopt(argv,"hi:o:t",["ifile=","ofile="])
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
            to_txt=True
    if ("-t" in sys.argv[1:])|("--txt" in sys.argv[1:]):
        to_txt=True
    if ('.mp3' in inputfile.lower())|('.wav' in inputfile.lower())|('.mp4' in inputfile.lower()):
        transcribe(inputfile,outputfile,to_txt)
    elif os.path.isdir(sys.argv[-1]):
        media_dir=sys.argv[-1]
        media_paths=[os.path.join(media_dir,item) for item in os.listdir(media_dir)]
        for pathname in media_paths:
            if pathname.lower()[-4:] in ('.wav','.mp3','.mp4'):
                transcribe(pathname,outputfile,to_txt)






if __name__ == "__main__":
   main(sys.argv[1:])







