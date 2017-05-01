from Tkinter import *
import ttk
from pygame import mixer
import numpy as np
import os
import time
import subprocess
import random
import csv
import datetime


#######################################
###### Enter Test Set Directory #######
########### & Speaker Value ###########
#######################################

test_set_dir = "/Volumes/U/AAPB_Corpus_May_2017/Test_Sets/AAPB_Test_Haystack_Baldwin"
speaker_value = "Baldwin, James"

#######################################


random.seed(1009)

mixer.pre_init(16000, -16, 1)

mixer.init()

counter=1

test_filenames = [item for item in os.listdir(test_set_dir) if item[-4:].lower() == '.wav']


test_clips_1_sec=[]


for filename in test_filenames:
    audio_pathname = os.path.join(test_set_dir,filename)
    basename = filename[:-4]
    segment_dir_pathname = os.path.join(test_set_dir,basename)
    try:
        os.mkdir(segment_dir_pathname)
        subprocess.call(['ffmpeg','-i',audio_pathname,'-n','-f','segment','-segment_time','1','-c','copy',os.path.join(segment_dir_pathname,basename+"_sec_%05d.wav")])
    except:
        print("Apparently already processed: "+filename)
    test_clips_1_sec += [os.path.join(segment_dir_pathname,item) for item in os.listdir(segment_dir_pathname) if item[-4:].lower() == '.wav']
    

random.shuffle(test_clips_1_sec)

os.chdir(test_set_dir)

current_file = test_clips_1_sec[0]     ## initializing global variable

def play_sound():
    global current_file
    global counter
    current_file=test_clips_1_sec.pop()
    print('\n'+str(counter))
    counter+=1
    print(current_file.split('/')[-1])
    time = float(current_file.split('_sec_')[-1].replace('.wav',''))
    print(str(datetime.timedelta(seconds=time)))
    f=mixer.Sound(current_file)
    f.play()

def repeat():
    f=mixer.Sound(current_file)
    f.play()


root = Tk()
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)


previous_file=''

ground_truth_filename = test_set_dir.strip('/').split('/')[-1]+'_ground_truth.csv'

fo=open(ground_truth_filename,'w')
csv_writer = csv.writer(fo)
    
csv_writer.writerow(['Basename','Time_in','Duration','Value','Additional_label'])


def write_primary_speaker(current_file):
    try:
        basename = current_file.split('/')[-1].split('_sec_')[0]
        if basename[-6:]=='.16000':
            basename = basename[:-6]
        time_in = str(float(current_file.split('_sec_')[-1].replace('.wav','')))
        csv_writer.writerow([basename,time_in,'1.0',speaker_value,''])
    except:
        print("ERROR: "+current_file)
    time.sleep(0.1)
    mixer.pause()
    mixer.init()
    play_sound()


def write_background(current_file):
    try:
        basename = current_file.split('/')[-1].split('_sec_')[0]
        if basename[-6:]=='.16000':
            basename = basename[:-6]
        time_in = str(float(current_file.split('_sec_')[-1].replace('.wav','')))
        csv_writer.writerow([basename,time_in,'1.0','background',''])
    except:
        print("ERROR: "+current_file)
    time.sleep(0.1)
    mixer.pause()
    mixer.init()
    play_sound()


def write_music(current_file):
    try:
        basename = current_file.split('/')[-1].split('_sec_')[0]
        if basename[-6:]=='.16000':
            basename = basename[:-6]
        time_in = str(float(current_file.split('_sec_')[-1].replace('.wav','')))
        csv_writer.writerow([basename,time_in,'1.0','background','music'])
    except:
        print("ERROR: "+current_file)
    time.sleep(0.1)
    mixer.pause()
    mixer.init()
    play_sound()



def launch_vlc(current_file):
    try:
        parent_filename = current_file.split('/')[-1].split('_sec_')[0]+'.wav'
        parent_pathname = os.path.join(test_set_dir,parent_filename)
        time_in = str(float(current_file.split('_sec_')[-1].replace('.wav','')))
        subprocess.call(["/Applications/VLC.app/Contents/MacOS/VLC", "--start-time="+str(time_in), parent_pathname])
    except:
        print("ERROR launching VLC: "+current_file)




yes_btn = ttk.Button(c, text=speaker_value, command= lambda: write_primary_speaker(current_file))
lbl2 = ttk.Label(c)
yes_btn.grid(column=0, row=1, sticky=N, pady=5, padx=5)
lbl2.grid(column=2, row=2, sticky=N, pady=5, padx=5)


music_btn = ttk.Button(c, text="Music", command= lambda: write_music(current_file))
lbl2 = ttk.Label(c)
music_btn.grid(column=0, row=3, sticky=N, pady=5, padx=5)
lbl2.grid(column=3, row=3, sticky=N, pady=5, padx=5)


no_btn = ttk.Button(c, text="Background", command= lambda: write_background(current_file))
lbl3 = ttk.Label(c)
no_btn.grid(column=0, row=2, sticky=N, pady=5, padx=5)
lbl3.grid(column=4, row=4, sticky=N, pady=5, padx=5)

rpt_btn = ttk.Button(c, text="Repeat", command=repeat)
lbl4 = ttk.Label(c)
rpt_btn.grid(column=0, row=4, sticky=N, pady=5, padx=5)
lbl4.grid(column=5, row=5, sticky=N, pady=5, padx=5)

rpt_btn = ttk.Button(c, text="Play in VLC", command= lambda: launch_vlc(current_file))
lbl4 = ttk.Label(c)
rpt_btn.grid(column=0, row=5, sticky=N, pady=5, padx=5)
lbl4.grid(column=6, row=6, sticky=N, pady=5, padx=5)





time.sleep(0.5)
play_sound()

root.mainloop()




fo.close()





#play and classify
#write classes to csv:
## Baldwin, 99.0, 1.0
## Background, 5.0, 1.0
## Baldwin, 976.0, 1.0

#Extract middle row to 2 lists of integers: background and Baldwin


#send smoothed gmm output to table and do the same
#true positive is intersection of ground truth positive seconds and machine positive
#true negative is intersection of ground truth negative and machine negative
#false positive is ground truth negative intersected with machine positive
#false negative is ground truth positive intersected with machine negative 

#Compare:
#Gmm
#Gmm smoothed 1x
#Gmm smoothed 2x
#Svm
#Svm smoothed 1x
#Svm smoothed 2x



