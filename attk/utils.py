#!/usr/bin/python

import sys, getopt
import os
import subprocess


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

working_dir = os.path.abspath('./')











if __name__ == "__main__":
   main(sys.argv)
