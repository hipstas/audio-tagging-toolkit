Install dependencies:

```bash
pip install -i dependencies.txt
```

Install FFmpeg with MP3 support:

```bash
add-apt-repository -y ppa:mc3man/trusty-media
apt-get update
apt-get -y dist-upgrade
apt-get -y install ffmpeg
```



Find applause in single file:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b -l "Speaker Name" -i /path/to/audio.mp3
```

Batch applause search:

```bash
cd /path/to/audio-tagging-toolkit

python FindApplause.py -c -b -l "Speaker Name" path/to/directory/
```

