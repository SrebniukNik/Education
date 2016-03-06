__author__ = 'srebnyuk_m'

#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def sort_uri(uri):
    print uri[-9],uri[-14]
    if uri[-9] == uri[-14]:
      print uri[-9],uri[-14]
      print uri[-8:-4]
      return uri[-8:-4]

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  print filename
  f = open(filename, 'rb')
  url_file = f.read()
  hostname = re.findall(r'\S+_(\S+)', filename)
  urls = re.findall(r"GET\s(\S+puzzle\S+)\sHTTP", url_file)
  puzzle_urls = set([])
  for url in urls:
      puzzle_urls.add('http://' + hostname[0] + str(url))
  return sorted(list(puzzle_urls), key=sort_uri)




def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  path = dest_dir
  path = os.path.abspath(path)
  print path
  if not os.path.exists(path):
    os.mkdir(os.path.abspath(path))
  index = open( path+"\index.html", 'a')
  index.write("<verbatim>\n<html>\n<body>\n")
  count = 0
  src = ''
  for url in img_urls:
    print url
    name = "\img" + str(count) + ".jpg"
    urllib.urlretrieve(url, path+name)
    src += "<img src=" + path+name + ">"
    count += 1
  index.write(src)
  index.write("\n</html>\n</body>")


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()