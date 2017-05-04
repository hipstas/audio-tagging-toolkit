## ATTK Classes & Functions

### __init__.py

### Diarize.py
    - class_list_to_time_rows
    - diarize
    - main

### ExcerptClass.py
    - create_tag_excerpt
    - main

### FindApplause.py         ## -> genericize to "Classify.py"
    - seconds_list_to_ranges
    - find_applause
    - main

### RandomTags.py
    - media_duration      ## -- to utils.py
    - random_tag
    - tags_to_csv
    - tags_to_wav
    - main

### Segment.py
    - excerpt_segments
    - main

### Transcribe.py
    - transcribe
    - main

## Todo

- Create `utils.py`
    - media_duration from RandomTags.py
    - create TagFile class to pass segments, pathname, and metadata between functions
