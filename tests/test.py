import os
import subprocess
import attk

audio_url = 'http://www.stephenmclaughlin.net/test_audio/29_Fried-Michael_10-17-03_ICA-UPenn_s25.213_d180.0.16000.wav'

audio_filename = audio_url.split('/')[-1]

subprocess.call(['wget','-y',audio_url])


duration = attk.RandomTags.media_duration(audio_filename)




attk.Diarize.diarize(audio_filename,audio_filename+'.csv',to_csv=True,plot=False,numSpeakers=0,buffer_secs=0)
