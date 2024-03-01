import json
import retrieve


initChar = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','other'] 

position = {}
fl = []
url = {}

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
        while True:
            user_input = input("Search: ")
            print("list at most 10 relevant url below")
            for i in retrieve.bool_retr(position,fl,user_input):
                print(url[i])
    except:
        print("exit")
        end()
        raise
    end()
    
