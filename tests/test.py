import os
import subprocess
import attk

audio_url = 'http://www.stephenmclaughlin.net/test_audio/29_Fried-Michael_10-17-03_ICA-UPenn_s25.213_d180.0.16000.wav'

audio_filename = audio_url.split('/')[-1]

subprocess.call(['wget',audio_url])


duration = attk.RandomTags.media_duration(audio_filename)
print(duration)

#audio_filename='/Volumes/U/AAPB_Corpus_May_2017/PennSound_UBM_for_Creeley_full_clips_16000/Cameron-David_01_HERE-Cafe_4-11-98_s70.708_d180.0.16000.wav'

attk.Diarize.diarize(audio_filename,audio_filename+'.csv',True,False,0,0)
