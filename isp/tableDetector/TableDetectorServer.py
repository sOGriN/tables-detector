'''
Created on Oct 9, 2019

@author: grigorii
'''
import socket 
import select
import sys
from isp.tableDetector.TableDetector import TableDetector
from http.server import SimpleHTTPRequestHandler, HTTPServer,\
    BaseHTTPRequestHandler
from _io import BytesIO
from _cffi_backend import callback
class HTTPProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        f = open('index.html','r')
        response_data = f.read()
        response_data = response_data.replace('$RESULT$', '')
        f.close()
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(response_data, 'utf-8'))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        print(b'\0x0d0a0d0a')
        print(b'\x0d\x0a\x0d\x0a')
        body = (self.rfile.read(content_length).split(b'\x0d\x0a\x0d\x0a')[1])
        
        f = open('index.html','r')
        response_data = f.read()
        f.close()
        
        answer = self.cbk(BytesIO(body))
        if answer == 'y':            
            response_data = response_data.replace('$RESULT$', 'Tables: yes')
        else:
            response_data = response_data.replace('$RESULT$', 'Tables: no')
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(response_data, 'utf-8'))
    def __init__(self, request, client_address, server, callback):
        self.cbk = callback
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

class HTTPServerClass(HTTPServer):
    def set_callback(self, callback):
        self.callback = callback
    def finish_request(self, request, client_address):
        HTTPProcessor(request, client_address, self, self.callback)

class TableDetectorServer(object):
    '''
    classdocs
    '''
    
    def __initializeTableDetector__(self, dirPath):
        self.tableDetector = TableDetector()
        self.tableDetector.trainFrom(dirPath)
    def __testPdf__(self, rawPdf):
        print('TEST: ' + rawPdf)
        #return self.tableDetector.predictFile(rawPdf)
    def startHTTPServer(self, port, dirPath):
        self.__initializeTableDetector__(dirPath)
        def callback(rawData):
            return self.tableDetector.predictFile(rawData)
        self.server_address = ('127.0.0.1', port)
        self.serv = HTTPServerClass(self.server_address, HTTPProcessor)
        self.serv.set_callback(callback)
        self.serv.serve_forever()
    def __init__(self):
        self.serv = None
        self.tableDetector = None
        '''
        Constructor
        '''
        