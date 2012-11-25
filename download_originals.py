import oauth2 as oauth
import urlparse
import sys
import time
import json

API_SECRET_FILE='.flickr.api-key.json'
ACCESS_TOKEN_SECRET_FILE='.flickr.access-token.json'

def main():
    fd = open(ACCESS_TOKEN_SECRET_FILE)
    access_token = json.loads(fd.read())
    fd.close()
    fd = open(API_SECRET_FILE)
    api_key = json.loads(fd.read())
    fd.close()
    consumer = oauth.Consumer(api_key['api_key'], api_key['api_key_secret'])
    token = oauth.Token(key=access_token['oauth_token'], secret=access_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    page = 1
    npages = 1000000
    while page <= npages:
        print >> sys.stderr, "retrieving page %d of %d" % (page, npages)
        resp, content = client.request('http://api.flickr.com/services/rest?format=json&method=flickr.photos.search&per_page=10&page=%d&user_id=%s&extras=url_o&nojsoncallback=1' % (page, access_token['user_nsid']))
        data = json.loads(content)
        page = int(data['photos']['page']) + 1
        npages = int(data['photos']['pages'])
        for photo in data['photos']['photo']:
            print photo['url_o']
        time.sleep(1)

if __name__ == '__main__':
    main()
