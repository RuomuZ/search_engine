import os
import re
import porter
import math
from collections import defaultdict as dd
import time
import threading


parsed_list = []
lock = threading.Lock()

def parse_str(i):
    global parsed_list
    temp = []
    for post in i.split("|"):
        b = post.split(".")
        b[1] = b[1].strip('][').split(', ')
        for l in range(len(b[1])):
            b[1][l] = int(b[1][l])
        b[2] = int(b[2])
        temp.append(b)
    with lock:
        parsed_list.append(temp)


#This function takes [str,str,str] as parameter where str here is the line just read, and each line 
#correspond to a word. This function parse those strings and return [[[doc_id,[position],frequency ],[next post]],[next word],[]]
def parse(post_str_list):
    global parsed_list
    threads = []
    for i in post_str_list:
        thread = threading.Thread(target=parse_str, args=(i,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    toReturn = parsed_list
    parsed_list = []
    return toReturn


# This function recursively find if all post lists contain the specific document id
def df_match(doc_id,list_slice):
    if len(list_slice) == 1:
        index = 0
        while int(list_slice[0][index][0]) <= int(doc_id):
            if int(list_slice[0][index][0]) == int(doc_id):
                return True
            index += 1
        return False
    else:
        if df_match(doc_id,list_slice[0:1]) and df_match(doc_id,list_slice[1:]):
            return True
        else:
            return False


def in_tag(tag_range,position):
    position_set = set(position)
    for start,end in tag_range:
        p_set = set(range(start,end))
        if len(set.intersection(position_set,p_set)) > 0:
            return True
    return False

doc_dict = {}
url_dict = {}

def score_process(word,idf): 
    global doc_dict,url_dict
    start = time.time()
    for post in word:
        if post[0] in doc_dict:
            tf = 1 + math.log(post[2],10)
            tfidf = tf * idf
            w = 0.1
            if in_tag(url_dict[post[0]][1],post[1]):      #title
                w = 1
            elif in_tag(url_dict[post[0]][2],post[1]):      #h1
                w = 0.8
            elif in_tag(url_dict[post[0]][3],post[1]):      #h2
                w = 0.6
            elif in_tag(url_dict[post[0]][4],post[1]):      #h3
                w = 0.4
            elif in_tag(url_dict[post[0]][5],post[1]):      #bold/strong
                w = 0.3
            with lock:
                #print(tf * idf)
                doc_dict[post[0]] += tf * idf * w
    end = time.time()


def score(l):
    global doc_dict
    global url_dict
    doc_dict = {}
    num_page = len(url_dict.keys())
    toScore = []
    for word in l:
        #print(f"score: {math.log(num_page/(len(word)),10)}")
        idf = math.log(num_page/(len(word)),10)
        if idf > 0.4:
            toScore.append((word[:100],idf))
    if len(toScore) == 0:
        toScore.clear()
        for word in l:
            toScore.append((word,0.2))
    s_id = []
    if len(toScore) == 1:
        for post in toScore[0][0]:
            doc_dict[post[0]] = 0
    else:
        for word,idf in toScore:
            temp = []
            for post in word:
                temp.append(post[0])
            s_id.append(set(temp))
        id_intersection = set()
        for i in range(len(s_id) - 1):
           for k in range(i,len(s_id) - 1):
                temp_inter = set.intersection(s_id[i],s_id[k+1])
                id_intersection = id_intersection.union(temp_inter)
        for i in id_intersection:
            doc_dict[i] = 0
    threads = []
    #print(toScore)
    for word,idf in toScore:
        thread = threading.Thread(target=score_process, args=(word,idf,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    temp_dict = doc_dict
    doc_dict = {}
    v_set = set([v for v in temp_dict.values()])
    temp_l = sorted(temp_dict.items(),key=lambda x: x[1],reverse=True)
    toReturn = []
    for k,v in temp_l:
        if v in v_set:
            toReturn.append(k)
            v_set.remove(v)
    return toReturn[0:10]

    
    
        
            



def retr(p, il, q,url):
    global url_dict
    url_dict = url
    myP = r"[a-z0-9]{2,23}"
    target_list = re.findall(myP,q.lower())
    post_list = []
    for i in range(len(target_list)):
        target_list[i] = porter.porter(target_list[i])
    token_set = set(target_list)
    #print(token_set)
    for token in token_set:
        token_init = ord(token[0])
        if token in p and token_init >= 97 and token_init <= 122:
            il[token_init - 97].seek(p[token])
            post_list.append(il[token_init - 97].readline().strip())
        elif token in p:
            il[26].seek(p[token])
            post_list.append(il[26].readline().strip())
    post_list = parse(post_list)
    post_list.sort(key=lambda x : len(x))
    toReturn = score(post_list)
    url_dict = {}
    return toReturn


#pl -> position, il -> index list, q -> query
#This function serve the boolean retrieval. It return a list of document id.

def bool_retr(p, il, q):
    myP = r"[a-z0-9]{2,23}"
    target_list = re.findall(myP,q.lower())
    post_list = []
    for i in range(len(target_list)):
        target_list[i] = porter.porter(target_list[i])
    token_set = set(target_list)
    #print(token_set)
    for token in token_set:
        token_init = ord(token[0])
        if token in p and token_init >= 97 and token_init <= 122:
            il[token_init - 97].seek(p[token])
            post_list.append(il[token_init - 97].readline().strip())
        elif token in p:
            il[26].seek(p[token])
            post_list.append(il[26].readline().strip())
    post_list = parse(post_list)
    #print(post_list)
    post_list.sort(key=lambda x : len(x))
    toReturn = []
    counter = 0
    if len(post_list) == 1:
        temp = post_list[0][:10]
        #print(f"temp: {temp}")
        for i in temp:
            toReturn.append(i[0])
        return toReturn
    elif len(post_list) > 1:
        for post in post_list[0]:
            if df_match(post[0],post_list[1:]):
                toReturn.append(post[0])
                counter += 1
            if counter >= 10:
                #print(toReturn)
                return toReturn
    #print(toReturn)
    return toReturn
