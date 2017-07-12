#!/usr/bin/python

import urllib2,urllib,hmac,base64,hashlib,sys,re,os,urlparse
from datetime import datetime

parameters = urlparse.parse_qs(os.environ['QUERY_STRING'])

if len(parameters) < 3:
  print 'Content-Type: text/html\n'
  print '<p>Not enough parameters... exiting.</p>'
  sys.exit()

keywords = str()
edsKey = parameters.get('key')[0]
search_type = parameters.get('st')[0]
kw = parameters.get('kw')[0]
keyword_list = kw.split()

for keyword in keyword_list:
  keywords += re.escape(keyword) + ' '

edsHost = 'widgets.ebscohost.com'
edsPath = '/prod/encryptedkey/eds/eds.php'
edsKey += 'MiOiJiMWU4YjA4YTA2MDMwYTdiIn0='
edsId = '&p=czUzMDgwMDQubWFpbi53c2FwaQ==&s=0,1,1,0,0,0'

if search_type == 'all':
  qstring = '&q=search%3Fquery=' + urllib.quote_plus(keywords)
  qstring += '%26view%3Ddetailed' # Detailed View
  qstring += '%26resultsperpage%3D10' # 10 Results per page
  qstring += '%26limiter%3DFT:y' # Show holdings only
elif search_type == 'article':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CJournal+Article%2Cfalse'
  qstring += '&s.ho=true' #Show holdings only
elif search_type == 'book':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CBook%2Cfalse'
  qstring += '&s.ho=true' #Show holdings only
elif search_type == 'journal':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CJournal%2Cfalse'
  qstring += '&s.ho=true' #Show holdings only
else:
  print 'Please specify search type.'
  sys.exit()

url = 'https://%s%s?%s%s%s' % (edsHost, edsPath, edsKey, edsId, qstring)
results = urllib2.urlopen(url).read()
print 'Content-Type: application/json\n'
print results
