__author__ = 'crumpet'

#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  f = open(filename, 'rU')
  baby_file = f.read()
  text = str(re.findall(r'Popularity\sin\s(\d\d\d\d)', baby_file)[0]) + "\n"
  babies = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', baby_file)
  unorder_babies = []
  #print baby_file

  for rank in babies:
    unorder_babies.append([rank[1], rank[0]])
    unorder_babies.append([rank[2], rank[0]])
  sorted_babies = sorted(unorder_babies)
  for baby in sorted_babies:
    text += str(baby[0]) + " " + str(baby[1]) + "\n"

  #print babies
  return text


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
  new_Args = []
  dir = open('dir.txt', 'wb')
  if "*" in str(args[0]):
    file = str(os.listdir("c:\Users\crumpet\PycharmProjects\BabyNames"))
    dir.write(file)
    dir.close()
    print file
    new_args = re.findall(r'(baby\d\d\d\d\.html)', file)
    print "matched filter", new_args
  else:
    new_args = args[:]

  summary_file = ""
  for arg in new_args:
    print arg
    summary_file = arg + ".summary"
    print summary_file
    summary = open(summary_file, 'wb')
    summary.write(extract_names(arg))
  print args

if __name__ == '__main__':
  main()
