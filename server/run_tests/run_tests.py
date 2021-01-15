import os
import sys

import nose

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))

import main


if __name__ == "__main__":
  nose.main()
