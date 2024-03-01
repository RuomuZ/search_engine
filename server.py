import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import os
import sys
import io 
import retrieve

PORT = 8000
initChar = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y',
        'z','other']
position = {}
fl = []
url = {}


def init():
    global fl, position, url
    fl = []
    url = {}
    position = {}
    with open("finalIndex/position.json","r") as f:
        position = json.load(f)
    with open("finalIndex/url_id_match.json","r") as f:
        url = json.load(f)
    for c in initChar:
        f = open(f"finalIndex/{c}.txt","r")
        fl.append(f)


def end():
    global fl
    for i in range(len(fl)):
        fl[i].close()


class myHttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server, directory=None):
        super().__init__(request,client_address,server,directory=None)

    def do_GET(self):
        global url,position,fl
        q = urlparse(self.path).query
        doc_ids = []
        if q != '':
            doc_ids = retrieve.bool_retr(position,fl,str((parse_qs(q))["search"][0]))
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
        for doc_id in doc_ids:
            output.write("<tr><th>"+url[doc_id]+"</th></tr>")
        output.write("</thead></table></body></html>")        
        self.wfile.write(output.getvalue().encode())
        return


Handler = myHttpHandler
if __name__ == "__main__":
    init()
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    except:
        end()
        raise
    end()
