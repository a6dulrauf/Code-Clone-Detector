#!/usr/bin/env python
"""Launch the Tkinter desktop UI for the Code Clone Detector."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from com.vsa.gui.gui import GUI

if __name__ == "__main__":
    GUI()
