import threading
import oauth2 as oauth
import urlparse
import urllib2
import json
import BaseHTTPServer

API_SECRET_FILE='.flickr.api-key.json'
ACCESS_TOKEN_SECRET_FILE='.flickr.access-token.json'


class ValidationHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()

    def do_GET(s):
        info = urlparse.parse_qsl(urlparse.urlparse(s.path).query)
        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write('<html><body>')
        for pair in info:
            s.wfile.write('%s: %s<br/>' % pair)
        s.wfile.write('</body></html>')

def run_http_server_one_request():
    server_address=('127.0.0.1', 8888)
    httpd = BaseHTTPServer.HTTPServer(server_address, ValidationHTTPRequestHandler)
    httpd.handle_request()
    

def main():
    fd = open(API_SECRET_FILE)
    contents = fd.read()
    print contents
    data = json.loads(contents)
    API_KEY=data['api_key']
    API_SECRET=data['api_key_secret']
    fd.close()
    request_token_url = 'http://www.flickr.com/services/oauth/request_token?oauth_callback=http://127.0.0.1:8888/validate'
    access_token_url = 'http://www.flickr.com/services/oauth/access_token'
    authorize_url = 'http://www.flickr.com/services/oauth/authorize'

    consumer = oauth.Consumer(API_KEY, API_SECRET)
    token = oauth.Token(key=API_KEY, secret=API_SECRET)
    client = oauth.Client(consumer)
    sig_method = oauth.SignatureMethod_HMAC_SHA1()
    resp, content = client.request(request_token_url)
    request_token = dict(urlparse.parse_qsl(content))
    print "Authorize URL: %s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    print 'Visit the Authorize URL and return here when you have added the required permission. You will need to copy the oauth_verifier code after you authorize access'
    #server_thread = threading.Thread(target=run_http_server_one_request)
    #server_thread.start()
    run_http_server_one_request()
    oauth_verifier = raw_input('Enter the validation code you see in the browser: ')
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url)
    #server_thread.join()
    access_token = dict(urlparse.parse_qsl(content))
    print "saving these to " + ACCESS_TOKEN_SECRET_FILE
    print "%s %s" % (access_token['oauth_token'],access_token['oauth_token_secret'] )
    fd = open(ACCESS_TOKEN_SECRET_FILE, 'w')
    fd.write(json.dumps(access_token))
    fd.close()

    print 'Done'

if __name__ == '__main__':
    main()
