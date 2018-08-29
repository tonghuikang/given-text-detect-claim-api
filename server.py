import time
import json
from http.server import *
from urllib.parse import urlparse
import pickle

import nlp_functions

HOST_NAME = '0.0.0.0'

import sys
myargs = sys.argv
if '-p' in myargs:
    try: PORT_NUMBER = int(myargs[2])
    except Exception as e:
        print(e)
        PORT_NUMBER = 4000
else:
    PORT_NUMBER = 4000

class IngestHandler(BaseHTTPRequestHandler):
#     def __init__(self):
#         super().__init__()
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # this should be loaded in init
        with open('processed_claims.pickle', 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            self.processed_claims = pickle.load(f)
            
        '''
        sample_input = {"article_text" : "State media Straits Times is talking about how Halimah is a puppet."}
        '''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            json_input = json.loads(post_data.decode('utf-8'))
            print(post_data)
        except:
            print(post_data)
            print("Invalid JSON Input")
        
        try: article_text = json_input["article_text"]
        except:
            article_text = "Lorem ipsum dolor sit amet."
            print(post_data)
            print("Invalid JSON Input")
        
        start = time.time()
        json_output = nlp_functions.article_against_claims(article_text, self.processed_claims)
        
        print("\nAnalysis took:", time.time()-start)
        print("\nJSON Output")
        print(json_output)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        parsed_path = urlparse(self.path)
        self.wfile.write(json_output.encode())
        return True
        
    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Potato</title></head>
        <body><p>This is a potato.</p>
        <p>You accessed potato path: {}</p>
        </body></html>
        '''.format(path)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)
        
        
if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), IngestHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))