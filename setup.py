from setuptools import setup
import os
from ez_setup import use_setuptools
use_setuptools()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='attk',
      version='0.0.3',
      description='Audio Tagging Toolkit: A collection of scripts to expedite audio annotation and classifier training.',
      url='https://github.com/hipstas/audio-tagging-toolkit',
      author='Stephen Reid McLaughlin',
      author_email='stephen.mclaughlin@utexas.edu',
      license='Apache 2.0',
      packages=['attk'],
      long_description=read('README.md'),
      classifiers=["Development Status :: 3 - Alpha"],
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
