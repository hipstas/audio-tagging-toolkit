
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os.path

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

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
