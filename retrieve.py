import os
import re
import porter

#This function takes [str,str,str] as parameter where str here is the line just read, and each line 
#correspond to a word. This function parse those strings and return [[[doc_id,[position],frequency ],[next post]],[next word],[]]
def parse(post_str_list):
    toReturn = []
    for i in post_str_list:
        temp = []
        for post in i.split("|"):
            b = post.split(".")
            b[1] = b[1].strip('][').split(', ')
            for l in range(len(b[1])):
                b[1][l] = int(b[1][l])
            b[2] = int(b[2])
            temp.append(b)
        toReturn.append(temp)
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
