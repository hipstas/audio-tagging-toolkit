#!/usr/bin/python

import sys, getopt
import os
import numpy as np
import librosa
import subprocess
from itertools import groupby
from operator import itemgetter
from numpy import ma
from aubio import source, pitch
from moviepy.audio.io import AudioFileClip


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

working_dir = os.path.abspath('./')


def main(argv):
   dd=1


def get_mfccs(wav_pathname):
   sample_array, sample_rate = librosa.load(wav_pathname)
   mfcc_frames = librosa.feature.mfcc(sample_array, sample_rate, hop_length=2048, n_mfcc=13).T
   mfcc_frames_sans_0th = [frame_values[1:] for frame_values in mfcc_frames]
   return mfcc_frames_sans_0th


def get_mfccs_and_deltas(wav_pathname):
   sample_array, sample_rate = librosa.load(wav_pathname)
   mfcc = librosa.feature.mfcc(sample_array, sample_rate, hop_length=2048, n_mfcc=13)
   delta = librosa.feature.delta(mfcc)
   delta2 = librosa.feature.delta(mfcc, order=2)
   mfcc = mfcc.T  ### Transposing tables
   delta = delta.T  ## (We can instead set the axis above to do this without the extra step)
   delta2 = delta2.T
   mfcc_sans_0th = [frame_values[1:] for frame_values in mfcc]
   all_features = []
   for i in range(len(mfcc)):
      all_features.append(list(mfcc_sans_0th[i]) + list(delta[i]) + list(delta2[i]))
   return all_features



def get_vowel_segments(media_path):
    downsample = 1
    samplerate = 44100 // downsample

    win_s = 2048 // downsample # fft size
    hop_s = 2048  // downsample # hop size

    s = source(media_path, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.6

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    samples=[]
    pitches=[]
    while True:
        samples, read = s()
        pitch_ = pitch_o(samples)[0]
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        pitches += [pitch_]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    pitches = np.array(pitches)
    confidences = np.array(confidences)

    cleaned_pitches = ma.masked_where(confidences < tolerance, pitches)
    cleaned_pitches = ma.masked_where(cleaned_pitches > 1000, cleaned_pitches)
    return list(np.logical_not(cleaned_pitches.mask))



def duration(media_path):
    return float(subprocess.check_output(['ffprobe', '-v', 'quiet', '-of', 'csv=p=0', '-show_entries', 'format=duration', media_path]).strip())


def smooth(x, window_len=10, window='hanning'):
        x=np.array(x)
        if x.ndim != 1:
           raise ValueError, "smooth only accepts 1 dimension arrays."
        if x.size < window_len:
           raise ValueError, "Input vector needs to be bigger than window size."
        if window_len < 3:
           return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
           raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        s = np.r_[2 * x[0] - x[window_len - 1::-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
        if window == 'flat':  # moving average
           w = np.ones(window_len, 'd')
        else:
           w = eval('np.' + window + '(window_len)')
        y = np.convolve(w / w.sum(), s, mode='same')
        return y[window_len:-window_len + 1]


seconds_list=[1,2,3,4,7,8,10,11,12,13]


def labels_to_ranges(seconds_list):
   ranges = []
   for k, g in groupby(enumerate(seconds_list), lambda (i, x): i - x):
      group = map(itemgetter(1), g)
      ranges.append((group[0], group[-1]))
   return ranges

labels_to_ranges(seconds_list)


def subclip(media_path):
        audio_filename=media_path.split('/')[-1]
        basename = audio_filename[:-4]
        start_time = round(float(row[1]),3)
        end_time = round(float(row[2]),3)
        snd = AudioFileClip.AudioFileClip(media_path)
        out_filename = basename+'__'+str(start_time)+'_'+str(end_time)+'.wav'
        snd.subclip(start_time,end_time).write_audiofile(out_filename)




#Display
#from IPython.display import display, Audio






if __name__ == "__main__":
   main(sys.argv)
