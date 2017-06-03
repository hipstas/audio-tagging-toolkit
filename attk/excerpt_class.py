#!/usr/bin/python

import os
import sys, getopt
import time, datetime
import subprocess

#here = os.path.abspath(os.path.dirname(__file__))
#sys.path.append(here)



def excerpt_class(media_path,csv_path,out_dir='',class_to_excerpt=1):
    try:
        basename=media_path.split('/')[-1][:-4]
    except:
        return("*** Problem loading basenames ***")
    try:
        from pydub import AudioSegment
        import pandas as pd
        import numpy as np
        tag_data = pd.read_csv(csv_path,header=None)
    except:
        print("*** Empty or missing tag CSV. ***")
        return("*** Empty or missing tag CSV. ***")
    try:
        includes_label=False
        if len(tag_data.iloc[0])==3:
            tag_data.columns=["Start","Class","Duration"]
        elif len(tag_data.iloc[0])==4:
            tag_data.columns=["Start","Class","Duration","Label"]
            includes_label=True
        if os.path.exists(media_path):
            if media_path.lower()[-4:].lower() in ('.wav','.mp3','.mp4'):
                if out_dir=='':
                    out_dir='/'.join(media_path.split('/')[:-1])+'/'
                basename = media_path.split('/')[-1][:-4]
                tag_data_relevant=tag_data[tag_data['Class']==class_to_excerpt]
                tag_data_relevant.reset_index(inplace=True)
                audio_source=True
                if media_path.lower()[-4:]=='.mp4':     # Creates a temporary WAV
                    audio_source=False                         # if input is MP4
                    temp_filename=media_path.split('/')[-1]+'_temp.wav'
                    audio_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
                    subprocess.call(['ffmpeg', '-y', '-i', media_path, audio_path]) # '-y' option overwrites existing file if present
                else:
                    audio_path=media_path
                song=None
                try:
                    if media_path[-4:].lower()=='.mp3':
                        song = AudioSegment.from_mp3(audio_path)
                    else:
                        song = AudioSegment.from_wav(audio_path)
                except:
                    print("Error loading audio with pyDub.")
                    return("Error loading audio with pyDub.")
                #### Batch extracting specified WAV clips ###
                for i in range(len(tag_data_relevant)):
                    #print("*** Extracting file "+str(i)+" of "+str(len(tag_data_relevant))+". ***\n")
                    #create_tag_excerpt(tag_data_relevant.iloc[i],audio_path,song,basename,out_dirincludes_label)
                    row=tag_data_relevant.iloc[i]
                    start = row['Start']
                    duration = row['Duration']
                    start_msec = float(start) * 1000.0
                    duration_msec = float(duration) * 1000
                    if includes_label==False:
                        clip_pathname=os.path.join(out_dir, basename+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(class_to_excerpt)+'.wav')
                    else:
                        clip_pathname=os.path.join(out_dir+basename+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(class_to_excerpt)+'_label_'+str(row['Label'])+'.wav')
                    if not os.path.exists(clip_pathname):
                        clip_data = song[start_msec:start_msec+duration_msec]
                        #clip_data=clip_data.set_channels(1)
                        clip_data.export(clip_pathname, format="wav")
                if audio_source==False:
                    os.remove(audio_path)
                #print("*** All segments extracted! ***")
            else: print("\n**Error: Not an acceptable media format. **\n")
        else: print("\n**Error: Audio file does not exist. **\n")
    except Exception as e: print(e)


def main(argv):
    media_path = ''
    class_to_excerpt = 1
    csv_path=''
    out_dir=''
    audio_source=True
    try:
        opts, args = getopt.getopt(argv[1:],"hi:t:e:o:",["ifile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            media_path = arg
            #print(arg)
        elif opt in ("-e", "--excerptclass"):
            class_to_excerpt = int(arg)
            #print(arg)
        elif opt in ("-t", "--tags"):
            csv_path=arg
            #print(csv_path)
        elif opt in ("-o", "--outdir"):
            out_dir=arg
            print("*** Audio output directory: "+out_dir)
        excerpt_class(media_path,csv_path,out_dir,class_to_excerpt)


if __name__ == "__main__":
   main(sys.argv)
