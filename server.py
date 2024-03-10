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

#initialization of files. fl contains all of the opened index files. url is a dictionary loaded from
#a json file under finalIndex directory named url_id_match.json. Position is a dictionary loaed from # position.json, contain all words and ther corresponding starting index. 
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

#this function close all files
def end():
    global fl
    for i in range(len(fl)):
        fl[i].close()

#This is the httphandler i wrote, serving the request
class myHttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server, directory=None):
        super().__init__(request,client_address,server,directory=None)

#This is the only function i override. It get the query, pass the query as parameter of bool_retr
#function I implemented in retrieve.py, and get a list of doc_id in return. Based on the id, 
#I can find the url in the dict url and fill the html content and respond to the user.
    def do_GET(self):
        global url,position,fl
        q = urlparse(self.path).query
        doc_ids = []
        if q != '':
            doc_ids = retrieve.retr(position,fl,str((parse_qs(q))["search"][0]),url)
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
            output.write("<tr><th>"+url[doc_id][0]+"</th></tr>")
        output.write("</thead></table></body></html>")        
        self.wfile.write(output.getvalue().encode())
        return


Handler = myHttpHandler
if __name__ == "__main__":
    init()
    #This host a server on localhost port 8000 and use my self-defined handler to serve request
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    #This will end after a key interrupt
    except:
        end()
        raise
    end()
