#!/usr/bin/python

# Most of this code came from https://gist.github.com/lawlesst/1070641
# This blog post also helped: http://blog.humaneguitarist.org/2014/09/04/getting-started-with-the-summon-api-and-python/
#
# Usage: 
# Place this file in your cgi-bin folder, make sure it is executable
# Your url should have a query string like this:
# http://yourserver.com/cgi-bin/summon_connector.py?id=your_summon_id&key=your_summon_key&st=all&kw=your+keywords

import urllib2,urllib,hmac,base64,hashlib,sys,re,os,urlparse
from datetime import datetime

parameters = urlparse.parse_qs(os.environ['QUERY_STRING'])
keywords = str()
api_id = parameters.get('kw')[0]
keyword_list = api_id.split()

for keyword in keyword_list:
  keywords += re.escape(keyword) + ' '

if len(parameters) < 4:
  print 'Content-Type: text/html\n'
  print '<p>Not enough parameters... exiting.</p>'
  sys.exit()

keywords = str()
api_id = parameters.get('id')[0]
api_key = parameters.get('key')[0]
search_type = parameters.get('st')[0]
kw = parameters.get('kw')[0]
keyword_list = kw.split()

for keyword in keyword_list:
  keywords += re.escape(keyword) + ' '

summonHost = 'api.summon.serialssolutions.com'
summonPath = '/2.0.0/search'

def summonMkHeaders(querystring):
  summonAccept = "application/json"
  summonThedate = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
  summonQS = "&".join(sorted(querystring.split('&')))
  summonQS = urllib.unquote_plus(summonQS)
  summonIdString = summonAccept + "\n" + summonThedate + "\n" + summonHost + "\n" + summonPath + "\n" + summonQS + "\n"
  summonDigest = base64.encodestring(hmac.new(api_key, unicode(summonIdString), hashlib.sha1).digest())
  summonAuthstring = "Summon "+api_id+';'+summonDigest
  summonAuthstring = summonAuthstring.replace('\n','')
  return {'Accept':summonAccept,'x-summon-date':summonThedate,'Host':summonHost,'Authorization':summonAuthstring}

if search_type == 'all':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CReference%2Ct'
  qstring += '&s.fvf=ContentType%2CBook+Review%2Ct'
  qstring += '&s.fvf=ContentType%2CResearch+Guide%2Ct'
  #FULL_TEXT_ONLINE:qstring += '&s.fvf=IsFullText%2Ctrue%2Cf'
elif search_type == 'article':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CJournal+Article%2Cfalse'
elif search_type == 'book':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CBook%2Cfalse'
elif search_type == 'journal':
  qstring = 's.q=' + urllib.quote_plus(keywords)
  qstring += '&s.fvf=ContentType%2CJournal%2Cfalse'
else:
  print 'Please specify search type.'
  sys.exit()
  
url = 'http://%s%s?%s' % (summonHost, summonPath, qstring)
headers = summonMkHeaders(qstring)
request = urllib2.Request(url=url, headers=headers)
results = urllib2.urlopen(request).read()
print 'Content-Type: application/json\n'
print results
