import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import os
import sys
import io 
import exp

PORT = 8000

class myHttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server, directory=None):
        super().__init__(request,client_address,server,directory=None)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        output = io.StringIO()
        output.write("<!doctype html><html lang='en'><head>"+
       "<title>Search Engine</title></head>"+ 
       "<body><h2>Search</h2><form id='search_form' method='get' action=index.html><label>" +
       "<input name='search' placeholder=''  type='text'>" +
      "</label></form>")
        output.write("<table><thead><tr><th>Title</th></tr>")
        output.write("<tr><th>"+exp.diy("blah")+"</th></tr>")
        output.write("</thead></table></body></html>")        
        self.wfile.write(output.getvalue().encode())
        return



Handler = myHttpHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
