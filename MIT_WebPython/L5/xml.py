__author__ = 'crumpet'

import urllib
from lxml import etree

#url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_185595.xml'

url = raw_input('Please enter your url to xml doc ')

urldata = urllib.urlopen(url)
print 'Retrieving', url

tree = etree.parse(urldata)

sum = 0

for element in tree.xpath('//count'):
  print element.text
  sum += int(element.text)

print "Total sum", sum
