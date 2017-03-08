from Tkinter import *
import ttk
from PIL import ImageTk, Image
from pygame import mixer
import numpy as np
import os
import time
import random

mixer.init()

#/Volumes/Turcich-2012/AAPB_excerpt_output_MLK_gradientboosting_Mar-8/
#/Volumes/Turcich-2012/AAPB_excerpt_output_MLK_SVM_Mar-8/

working_dir='/Volumes/Turcich-2012/AAPB_excerpt_output_MLK_SVM_Mar-8/'

classifier_name='MLK_SVM'


os.chdir(working_dir)

filenames=sorted([item for item in os.listdir(working_dir) if item!='.DS_Store'])

random.shuffle(filenames)

current_file=filenames[0]

def play_sound():
    print current_file
    global current_file
    current_file=filenames.pop()
    f=mixer.Sound(current_file)
    f.play()

def repeat():
    f=mixer.Sound(current_file)
    f.play()


def showImage():
        lbl1.configure(image=image_tk)
        btn.configure(text = "load image!", command=showImage1)

def showImage1(): 
        lbl1.configure(image=image_tk1)
        btn.configure(text = "load image!", command=showImage)     

root = Tk()    
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

#fname = "/Users/mclaugh/Desktop/sound_imgs/1.jpg"
#image_tk = ImageTk.PhotoImage(Image.open(fname))

#fname1 = "/Users/mclaugh/Desktop/sound_imgs/2.png"
#image_tk1 = ImageTk.PhotoImage(Image.open(fname1))  # new image object

previous_file=''

try:
    with open(working_dir+'_'+classifier_name+'_evaluation.txt') as fi:
        previous_file = fi.read()
except: pass

fo=open(working_dir+'_'+classifier_name+'_evaluation.txt','w')

fo.write(previous_file+'\n')


def write_yes():
    fo.write('''"'''+current_file+'''"'''+', correct\n')
    time.sleep(0.1)
    mixer.pause()
    mixer.init()
    play_sound()

def write_no():
    fo.write('''"'''+current_file+'''"'''+', incorrect\n')
    time.sleep(0.1)
    mixer.stop()
    mixer.init()
    play_sound()

def write_music():
    fo.write('''"'''+current_file+'''"'''+', music\n')
    time.sleep(0.1)
    mixer.stop()
    mixer.init()
    play_sound()





#btn = ttk.Button(c, text="load image", command=showImage)
#lbl1 = ttk.Label(c)
#btn.grid(column=0, row=0, sticky=N, pady=5, padx=5)
#lbl1.grid(column=1, row=1, sticky=N, pady=5, padx=5)

yes_btn = ttk.Button(c, text="yes", command=write_yes)
lbl2 = ttk.Label(c)
yes_btn.grid(column=0, row=1, sticky=N, pady=5, padx=5)
lbl2.grid(column=2, row=2, sticky=N, pady=5, padx=5)


music_btn = ttk.Button(c, text="music", command=write_music)
lbl2 = ttk.Label(c)
music_btn.grid(column=0, row=3, sticky=N, pady=5, padx=5)
lbl2.grid(column=3, row=3, sticky=N, pady=5, padx=5)




no_btn = ttk.Button(c, text="no", command=write_no)
lbl3 = ttk.Label(c)
no_btn.grid(column=0, row=2, sticky=N, pady=5, padx=5)
lbl3.grid(column=4, row=4, sticky=N, pady=5, padx=5)

rpt_btn = ttk.Button(c, text="repeat", command=repeat)
lbl4 = ttk.Label(c)
rpt_btn.grid(column=0, row=4, sticky=N, pady=5, padx=5)
lbl4.grid(column=5, row=5, sticky=N, pady=5, padx=5)



time.sleep(0.5)
play_sound()

root.mainloop()

fo.close()

















