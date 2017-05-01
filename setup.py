from setuptools import setup

setup(name='attk',
      version='0.0.3',
      description='Audio Tagging Toolkit: A collection of scripts to expedite audio annotation and classifier training.',
      url='https://github.com/hipstas/audio-tagging-toolkit',
      author='Stephen Reid McLaughlin',
      author_email='stephen.mclaughlin@utexas.edu',
      license='Apache 2.0',
      packages=['attk'],
      install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-learn==0.18',
        'pyperclip',
        'pydub',
        'ffprobe',
        'speechrecognition',
        'pocketsphinx',
        'pyAudioAnalysis',
        'tqdm'
      ],
      keywords='audio music speech classification tagging labeling ml supervised',
      zip_safe=False)
