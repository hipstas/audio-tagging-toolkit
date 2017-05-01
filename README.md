
### Mac Installation


Install Audio Tagging Toolkit using pip:

```bash
pip install git+git://github.com/hipstas/audio-tagging-toolkit.git
```

Next we will install **`ffmpeg`**, a command-line tool for audio and video encoding. First we will install several media codecs and command-line tools, then we will download ffmpeg's source code and compile it before installing. If you've previously installed ffmpeg using Homebrew, uninstall that copy before we begin:

```bash
brew uninstall ffmpeg
```

Enter the following commands one at a time; note that the first and fourth lines are very long. After the last command you will be prompted to enter your password.

```
brew install automake fdk-aac git lame libass libtool libvorbis libvpx opus sdl shtool texi2html theora wget x264 xvid yasm

git clone http://source.ffmpeg.org/git/ffmpeg.git ffmpeg

cd ffmpeg

./configure  --prefix=/usr/local --enable-gpl --enable-nonfree --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libxvid

make && sudo make install
```



### Install Ubuntu dependencies:

```bash
apt-get update -y && apt-get upgrade -y
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
sudo apt-get -y install swig
sudo apt-get -y install libpulse-dev

pip install -U pip
pip install virtualenv

#Install FFmpeg with MP3 support (at your own risk):

sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get -y dist-upgrade
sudo apt-get -y install ffmpeg
```

Now install Audio Tagging Toolkit using pip:

```bash
pip install git+git://github.com/hipstas/audio-tagging-toolkit.git
```





### Script examples via bash

- Locate applause in single file, with non-applause segments labeled "Speaker Name" and a 2-second buffer on either side of each transition:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b 2 -l "Speaker Name" -i /path/to/audio.mp3
```

- Batch applause classification with CSV output, default 1-second buffer, and label for non-applause regions:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b -l "Speaker Name" /path/to/directory/
```

- Diarize a single file:

```bash
cd /path/to/audio-tagging-toolkit

python Diarize.py -b -c -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3
```

- Batch Diarize:

```bash
cd /path/to/audio-tagging-toolkit

python Diarize.py -b -c /Users/mclaugh/Desktop/attktest/
```

- Excerpt a class:

```bash

cd /Users/mclaugh/Dropbox/WGBH_ARLO_Project/audio-tagging-toolkit/

for f in /Volumes/Turcich-2012/AAPB_Test_Haystack/*_king_gradientboosting.csv; do
base=$(basename """$f""" _king_gradientboosting.csv)
python ExcerptClass.py -i """/Volumes/Turcich-2012/AAPB_Test_Haystack/$base.mp3""" -t """$f""" -e 0 -o "/Volumes/Turcich-2012/AAPB_excerpt_output/";
done

for f in /Volumes/Turcich-2012/AAPB_Test_Haystack/*_king_gradientboosting.csv; do
base=$(basename """$f""" _king_gradientboosting.csv)
python ExcerptClass.py -i """/Volumes/Turcich-2012/AAPB_Test_Haystack/$base.mp4""" -t """$f""" -e 0 -o "/Volumes/Turcich-2012/AAPB_excerpt_output/";
done
```

- Excerpt from MP4s only:

```bash
cd /Users/mclaugh/Dropbox/WGBH_ARLO_Project/audio-tagging-toolkit/

for f in /Volumes/Turcich-2012/AAPB_Test_Haystack/*.mp4; do
base=$(basename """$f""" .mp4)
command="""python ExcerptClass.py -i "/Volumes/Turcich-2012/AAPB_Test_Haystack/$base.mp4" -t "/Volumes/Turcich-2012/AAPB_Test_Haystack/${base}_king_gradientboosting.csv" -e 0 -o "/Volumes/Turcich-2012/AAPB_excerpt_output/" """;
echo $command
eval $command;
done
```

- Launch QuickCheck script to rapidly review applause/speaker labels in Sonic Visualiser:

```bash
cd /path/to/audio-tagging-toolkit
python QuickCheck.py -a -v -i /path/to/audio/files
```

- QuickCheck diarization mode:


```bash
cd /path/to/audio-tagging-toolkit
python QuickCheck.py -d -v -i /path/to/audio/files
```

- Assign random tags:

```bash
python RandomTags.py -s 3 -n 3 -e -i /path/to/example.mp3 -o /path/to/output_dir/
```
