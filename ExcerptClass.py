#!/usr/bin/python

import os
import sys, getopt
import time, datetime
import subprocess



def create_tag_excerpt(row,audio_path,song):
    from pydub import AudioSegment
    start = row['Start']
    duration = row['Duration']
    start_msec = float(start) * 1000.0
    duration_msec = float(duration) * 1000
    if len(row)<=6:
        clip_pathname=row['Out Directory']+row['Basename']+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(row['Class'])+'.wav'
    elif len(row)>6:
        clip_pathname=row['Out Directory']+row['Basename']+"_start_"+str(start)[:6]+"_dur_"+str(duration)[:6]+'_class_'+str(row['Class'])+'_label_'+str(row['Label'])+'.wav'
    if not os.path.exists(clip_pathname):
        
        clip_data = song[start_msec:start_msec+duration_msec]
        #clip_data=clip_data.set_channels(1)
        clip_data.export(clip_pathname, format="wav")    
        


inputfile = ''


def main(argv):
    inputfile = ''
    excerpt_class = 0
    tag_path=''
    out_dir=''
    wav_source=True
    try:
        opts, args = getopt.getopt(argv,"hi:t:e:o:",["ifile="])
    except getopt.GetoptError:
        print ""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            #print(arg)
        elif opt in ("-e", "--excerptclass"):
            excerpt_class = int(arg)
            #print(arg)
        elif opt in ("-t", "--tags"):
            tag_path=arg
            #print(tag_path)
        elif opt in ("-o", "--outdir"):
            out_dir=arg
            print("*** Audio output directory: "+out_dir)

    try:
    
        done_basenames=[item.split('_start')[0] for item in os.listdir(out_dir) if '_start_' in item]
        done_basenames=sorted(list(set(done_basenames)))
        
        basename=inputfile.split('/')[-1][:-4]
        if basename in done_basenames:
            print("*** Basename already processed. ***")
            return("*** Basename '"+basename+"' already processed. ***")
    
    except:
        print("*** Problem loading basenames ***")
        os.remove(out_dir+'/'+basename+'_start_placeholder.txt')
        return("*** Problem loading basenames ***")
    
    try:
        from pydub import AudioSegment
        import pandas as pd
        import numpy as np
        
        tag_data = pd.read_csv(tag_path,header=None)
    
    except:
        print("*** Empty or missing tag CSV. ***")
        return("*** Empty or missing tag CSV. ***")
    
    try:
        if len(tag_data.iloc[0])==3:
            tag_data.columns=["Start","Class","Duration"]
        elif len(tag_data.iloc[0])==4:
            tag_data.columns=["Start","Class","Duration","Label"]

    
        if os.path.exists(inputfile):

    
            if inputfile.lower()[-4:].lower() in ('.wav','.mp3','.mp4'):
    
                tag_data['Pathname']=inputfile
        
                if out_dir=='':
                    out_dir='/'.join(inputfile.split('/')[:-1])+'/'
                    tag_data['Out Directory']=out_dir
                else:
                    tag_data['Out Directory']=out_dir
        
                basename = inputfile.split('/')[-1][:-4]
            
                tag_data['Basename'] = basename
        
                tag_data_relevant=tag_data[tag_data['Class']==excerpt_class]
        
                if basename not in done_basenames:
                
                    try:
                        with open(out_dir+'/'+basename+'_start_placeholder.txt','w') as fo:
                            fo.write('\n# placeholder\n')
                        print("Wrote placeholder file.")
                    except: pass
                
                
                    wav_source=True
                    if inputfile.lower()[-4:]=='.mp4':     # Creates a temporary WAV
                        wav_source=False                         # if input is MP4
                        temp_filename=inputfile.split('/')[-1]+'_temp.wav'
                        audio_path='/var/tmp/'+temp_filename   # Pathname for temp WAV
                        subprocess.call(['ffmpeg', '-y', '-i', inputfile, audio_path]) # '-y' option overwrites existing file if present
                    else:
                        audio_path=inputfile


                    song=None
                    
                    try:
                        if inputfile[-4:].lower()=='.mp3':
                            song = AudioSegment.from_mp3(audio_path)
                        else:
                            song = AudioSegment.from_wav(audio_path)
                    except:
                        print("Error loading audio with pyDub.")
                        os.remove(out_dir+'/'+basename+'_start_placeholder.txt')
                        return("Error loading audio with pyDub.")



                    #### Batch extracting specified WAV clips ###
                    for i in range(len(tag_data_relevant)):
                        print("*** Extracting file "+str(i)+" of "+str(len(tag_data_relevant))+". ***\n")
                        create_tag_excerpt(tag_data_relevant.iloc[i],audio_path,song)
                  
                    try:
                        os.remove(out_dir+basename+'_start_placeholder.txt')
                    except:
                        pass
                    
                    if wav_source==False:
                        os.remove(audio_path)

                    
                    print("*** All segments extracted! ***")
                    
                else: print("\n** Basename already processessed. **\n")
            else: print("\n** Not an acceptable media format. **\n")
        else: print("\n** Audio file does not exist. **\n")


        

    except:
        print("Some error.")

    print("*** Reached end of script. ***\n\n")


if __name__ == "__main__":
   main(sys.argv[1:])





