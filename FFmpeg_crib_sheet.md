## Convert all MP3s in a directory to mono 16/44.1 WAVs

```bash
cd /path/to/directory

for file in *.mp3; 
do ffmpeg -i $file -acodec pcm_s16le -ac 1 `basename "$file" .mp3`.wav; 
done
```

