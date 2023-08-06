import sys
import ctypes
import os

# add this directory to the system path  (this is a terrible hack)
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)

from omniORB import CORBA
import AAS_CORBA
