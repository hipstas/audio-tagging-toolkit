#!/usr/bin/python

import sys, getopt
import os
import pyperclip
import subprocess
import random
import time






def main(argv):
    working_dir=''
    applause=False
    diarized=False
    sleep_time=7.0
    try:
        opts, args = getopt.getopt(argv,"hi:das:",["input="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "'"
            sys.exit()
        elif opt in ("-i", "--in"):
            working_dir = arg
        elif opt in ("-s", "--sleep"):
            sleep_time=float(5)
    if "-d" in sys.argv[1:]:
        diarized=True
    if "-a" in sys.argv[1:]:
        applause=True

    if (diarized & applause):
        print "QuickCheck can only run in one mode at a time, either 'applause' or 'diarized.' Remove one of these options to continue."
        sys.exit()
    elif not (diarized | applause):
        print "Please specify 'applause' (-a) or 'diarized' (-d) mode."
        sys.exit()
    if working_dir=='':
        print "Please specify working directory with -i."
        sys.exit()
        
    temp=raw_input("\nQuickCheck will copy text to your clipboard, overwriting its current contents. Press return to continue. ")

    if applause==True:
        csv_ending='_applause.csv'
    elif diarized==True:
        csv_ending='_diarized.csv'

    filenames=os.listdir(working_dir)
    
    random.shuffle(filenames)
    
    if working_dir[-1]!='/':
        working_dir=working_dir+'/'
    
    media_filenames=[item for item in filenames if item.lower()[-4:] in ('.mp3','.wav','.mp4')]
    
    for filename in media_filenames:
        basename=os.path.splitext(os.path.basename(filename))[0]
        csv_filename=basename+csv_ending
        if (basename+'_corrected.csv' not in filenames)&(csv_filename in filenames):
            media_path=working_dir+filename
            csv_path=working_dir+csv_filename
            pyperclip.copy(basename+'_corrected.csv')
            print "\nFilename for corrected csv (copied to clipboard): "+basename+'_corrected.csv\n'
            subprocess.call(['open', '-a', 'Sonic Visualiser', media_path])
            time.sleep(sleep_time)
            subprocess.call(['open', '-a', 'Sonic Visualiser', csv_path])
            temp=raw_input("Press return to check next file. ")








if __name__ == "__main__":
   main(sys.argv[1:])

