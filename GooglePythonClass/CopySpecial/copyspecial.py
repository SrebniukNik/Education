__author__ = 'srebnyuk_m'
#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil

"""Copy Special exercise
"""

def get_special_paths(dirs):
  """
  returns a list of the absolute paths of the special files in the given directory
  """
  file_paths = []
  abs_path = []
  for dir in dirs:
      filenames = []
      filenames += os.listdir(dir)
      for filename in filenames:
        file_paths.append( os.path.join(dir, filename) )
  for file_path in file_paths:
    if re.findall(r'__\w+__', file_path):
      print "BINGO", os.path.abspath(file_path)
      abs_path.append(os.path.abspath(file_path))
  return abs_path

# +++your code here+++
# Write functions and modify main() to call them

def copy_to(path, dirs):
  abspath = ''
  abspath = os.path.abspath(path)
  if not os.path.exists(abspath):
    os.mkdir(abspath)
  files = get_special_paths(dirs)
  for file in files:
    shutil.copy(file, abspath)

def zip_to(paths, tozip):
  abspath = ''
  abszip = os.path.abspath(tozip)
  files = get_special_paths(paths)
  print files
  for file in files:
    cmd = '"C://Program Files (x86)//7-Zip//7z.exe"' + " a " + abszip + " " + str(file)
    try:
      os.system(cmd)
    except IOError:
      sys.stderr.write('problem zipping:' + str(abszip))


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]"
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  paths = args[:]
  if paths and not (todir or tozip):
    get_special_paths(paths)
  elif todir:
    copy_to(todir, paths)
  elif tozip:
    zip_to(paths, tozip)


if __name__ == "__main__":
  main()
