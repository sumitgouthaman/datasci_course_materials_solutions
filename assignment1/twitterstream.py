import oauth2 as oauth
import urllib2 as urllib
import sys
import json

# See assignment1.html instructions or README for how to get these credentials

# Modifed to read keys in a json format from another
# So that the other file can be ignored from git

try:
  keys_file = open("~twitter_api_keys.txt", "r")
  keys_json = json.loads(keys_file.read())
except IOError:
  print "File ~twitter_api_keys.txt not found or not in proper format!"
  sys.exit(1)

try:
  api_key = keys_json[u'api_key']
  api_secret = keys_json[u'api_secret']
  access_token_key = keys_json[u'token_key']
  access_token_secret = keys_json[u'token_secret']
except KeyError:
  print "Required keys not found in json from ~twitter_api_keys.txt"
  sys.exit(1)

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json?lang=en"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

if __name__ == '__main__':
  fetchsamples()
