import json
import retrieve
import time

initChar = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','other'] 

position = {}
fl = []
url = {}


#initialization function excatly the same as the one in server.py
def init():
    global fl, position,url
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


if __name__ == "__main__":
    init()
    try:
    #As a console text interface, it is just a while loop that keeps taking input and show at most
    #10 results. It ends after a key interrupt.
        while True:
            user_input = input("Search: ")
            start = time.time()
            print("list at most 10 relevant url below")
            for i in retrieve.retr(position,fl,user_input,url):
                print(url[i][0])
            end = time.time()
            print(f"time used: {end - start}")
    except:
        print("exit")
        end()
        raise
    end()
    
