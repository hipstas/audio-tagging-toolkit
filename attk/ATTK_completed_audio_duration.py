$$ Checks total duration of ATTK-tagged audio segments in a given directory.

import os


def time_completed(dir_path):
    pathnames=[os.path.join(dir_path,filename) for filename in os.listdir(dir_path)]
    corrected_files=sorted([item for item in pathnames if '_corrected.csv' in item])
    csv_set=[]
    for pathname in corrected_files:
        with open(pathname) as fi:
            csv_set.append(fi.read().splitlines())
    tagged_duration=0.0
    for table in csv_set:
        for row in table:
            cells=row.split(',')
            if len(cells)>2:
                duration=float(cells[2])
                tagged_duration=duration+tagged_duration
    return str(tagged_duration/60.0/60.0) + ' hours'


dir_path='/Users/mclaugh/Dropbox/WGBH_ARLO_Project/Extended_Corpus/Malcolm_X'

time_completed(dir_path)


