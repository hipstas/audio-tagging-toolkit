#!/usr/bin/python

import sys, getopt
import os
import pyperclip
import subprocess
import random
import time
from time import gmtime, strftime



def main(argv):
    working_dir=''
    applause=False
    diarized=False
    sleep_time=5.0
    launch_video=False
    script_path=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        opts, args = getopt.getopt(argv[1:],"hi:das:v",["input="])
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
            sleep_time=float(arg)
    if "-d" in sys.argv[1:]:
        diarized=True
    if "-a" in sys.argv[1:]:
        applause=True
    if "-v" in sys.argv[1:]:
        launch_video=True

    if (diarized & applause):
        print "QuickCheck can only run in one mode at a time, either 'applause' or 'diarized.' Remove one of these options to continue."
        sys.exit()
    elif not (diarized | applause):
        print "Please specify 'applause' (-a) or 'diarized' (-d) mode."
        sys.exit()
    if working_dir=='':
        print "Please specify working directory with -i."
        sys.exit()


    if applause==True:
        csv_ending='_applause.csv'
    elif diarized==True:
        csv_ending='_diarized.csv'

    filenames=os.listdir(working_dir)

    random.shuffle(filenames)

    if working_dir[-1]!='/':
        working_dir=working_dir+'/'

    media_filenames=[item for item in filenames if item.lower()[-4:] in ('.mp3','.wav','.mp4')]
    corrected_media_files=[item for item in media_filenames if item[:-4]+'_corrected.csv' in filenames]

    print str(len(media_filenames))+" media files in directory, "+str(len(corrected_media_files))+" corrected so far"

    no_audio_tags=[]

    temp=raw_input("\n*** QuickCheck will copy text to your clipboard, overwriting its current contents. Press return to continue. ***\n\n")


    for filename in media_filenames:
        basename=os.path.splitext(os.path.basename(filename))[0]
        csv_filename=basename+csv_ending
        if (basename+'_corrected.csv' not in filenames)&(csv_filename in filenames):
            if open(working_dir+csv_filename).read()=='':
                no_audio_tags.append(filename)
            else:
                media_path=working_dir+filename
                csv_path=working_dir+csv_filename
                pyperclip.copy(basename+'_corrected.csv')
                print "\n  > Filename for corrected CSV (copied to clipboard): "+basename+'_corrected.csv\n'
                subprocess.call(['open', '-a', 'Sonic Visualiser', media_path])
                if (launch_video==True)&(filename[-4:]=='.mp4'):
                    subprocess.call(['open', '-a', 'VLC', media_path])
                time.sleep(sleep_time)
                subprocess.call(['open', '-a', 'Sonic Visualiser', csv_path])
                temp=raw_input("Press return to check next file. ")

                if os.path.isfile(working_dir+basename+'_corrected.csv'):
                    with open(working_dir+basename+'_corrected.csv') as fi:
                        temp_csv=fi.read()
                    with open(working_dir+basename+'_corrected.csv','w') as fo:
                        fo.write(temp_csv)
                        fo.write('\n\n## Edited by '+str(os.getlogin()))
                        fo.write('\n## '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+' GMT')

    print "\nLooks like you've finished this batch. Nice work!\n"
    if len(no_audio_tags)>0:
        print "These files' CSVs contain zero tags:"
        for filename in no_audio_tags:
            print filename




if __name__ == "__main__":
   main(sys.argv)
