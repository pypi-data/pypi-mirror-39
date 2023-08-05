#!/usr/bin/env python
import os, sys
print('This is my test module __main__.py', __name__ )
if not __package__:
  path = os.path.join(os.path.dirname(__file__), os.pardir)
  sys.path.insert(0, path)

from re_name import renamer
renamer.Renamer().update()
