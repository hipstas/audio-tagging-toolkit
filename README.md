The basics:

```bash
apt-get update -y && apt-get upgrade -y
pip install -U pip
pip install --user virtualenv
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
sudo apt-get -y install swig
sudo apt-get -y install libpulse-dev
```

Install FFmpeg with MP3 support (at your own risk):

```bash
sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get -y dist-upgrade
sudo apt-get -y install ffmpeg
```

Create virtual environment:

```bash
virtualenv attk_env
source attk_env/bin/activate
#deactivate
```

Install dependencies:

```bash
sudo pip install -r requirements.txt
```
>Note: Let me know if this dependency list is incomplete for your system: stephen.mclaughlin@utexas.edu

Locate applause in single file, with non-applause segments labeled "Speaker Name" and a 2-second buffer on either side of each transition:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b 2 -l "Speaker Name" -i /path/to/audio.mp3
```

Batch applause classification with CSV output, default 1-second buffer, and label for non-applause regions:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b -l "Speaker Name" /path/to/directory/
```

Diarize a single file:

```bash
cd /path/to/audio-tagging-toolkit

python Diarize.py -b -c -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3
```

Batch Diarize:

```bash
cd /path/to/audio-tagging-toolkit

python Diarize.py -b -c /Users/mclaugh/Desktop/attktest/
```

Excerpt a class:

```bash
for f in /Volumes/Turcich-2012/AAPB_Test_Haystack/*_king_gradientboosting.csv; do
python ExcerptClass.py ;
done
```



Launch QuickCheck script to rapidly review applause/speaker labels in Sonic Visualiser:

```bash
cd /path/to/audio-tagging-toolkit
python QuickCheck.py -a -v -i /path/to/audio/files
```

QuickCheck diarization mode:


```bash
cd /path/to/audio-tagging-toolkit
python QuickCheck.py -d -v -i /path/to/audio/files
```
