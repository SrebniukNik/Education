__author__ = 'crumpet'

import urllib
import json

#serviceurl = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_42.json'
serviceurl = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_185599.json'

uh = urllib.urlopen(serviceurl)
data = uh.read()
print 'Retrieved',len(data),'characters'

info = json.loads(data)
#print json.dumps(info, indent=2)

count = 0
sum = 0

for item in info['comments']:
  #print item
  sum += int(item['count'])
  count += 1

print "Count", count
print "Total sum", sum
