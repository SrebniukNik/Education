__author__ = 'crumpet'

import urllib
from BeautifulSoup import *
import re

url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_185598.html'

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
tags = soup.findAll(name='span', text=True)
sum_total = 0

for tag in tags:
   # Look at the parts of a tag
   if re.match('\d+', tag):
       sum_total += int(tag)

print "Sum total ", sum_total

