__author__ = 'crumpet'

import urllib
from BeautifulSoup import *
import re

#url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Fikret.html'
url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Raniyah.html'


#for i in range(0,4):
for i in range(0,7):
  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html)
  tags = soup(href=True)
  #href = str(tags[2])
  href = str(tags[17])
  url = re.findall('(http:.+?html)', href)[0]
  print "New url is", url
  print "Name is", re.findall('\">(.+?)</a', href)[0]


