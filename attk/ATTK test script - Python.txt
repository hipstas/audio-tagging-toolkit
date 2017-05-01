import os

def test():
	os.chdir('/Users/mclaugh/Dropbox/WGBH_ARLO_Project/audio-tagging-toolkit/')
	try:
		os.system('python Diarize.py -b -c -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3')
		os.system('python FindApplause.py -c -b -l "Robert Creeley" -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3')
		os.system('python Transcribe.py -t -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3')
		os.system('python FindApplause.py -c -b -l "Robert Creeley" /Users/mclaugh/Desktop/attktest/')
		os.system('python ExcerptClass.py -i /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2.mp3 -t /Users/mclaugh/Desktop/attktest/Creeley-Robert_33_A-Note_Rockdrill-2_diarized.csv -e 1 -o /Users/mclaugh/Desktop/attktest/')
		print "****** Individual files worked ******"
		os.system('python Diarize.py -b -c /Users/mclaugh/Desktop/attktest/')
		os.system('python Transcribe.py -c /Users/mclaugh/Desktop/attktest/')
		os.system('python Transcribe.py -t /Users/mclaugh/Desktop/attktest/')
		print "HEY, you did it!"
	except:
		print "ERROR at some point ..."


test()

