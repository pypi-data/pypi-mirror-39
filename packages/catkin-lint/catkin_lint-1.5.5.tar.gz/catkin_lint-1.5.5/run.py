#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from catkin_lint.main import main
main()

