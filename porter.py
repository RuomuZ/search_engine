import re

v = ['a','e','i','o','u']
v_wxy = ['a','e','i','o','u','x','Y','z']
valid_LI = ['c','d','e','g','h','k','m','n','r','t']
db = ['b','d','f','g','m','n','p','r','t']
p_ex = ['gener','commun','arsen']
except1 = {"skis":"ski","skies":"sky","dying":"die","lying":"lie","tying":"tie","idly":"idl","gently":"gentl","ugly":"ugli",
        "early":"earli","only":"onli","singly":"singl", "sky":"sky","news":"news","howe":"howe","atlas":"atlas","cosmos":"cosmos",
        "bias":"bias","andes":"andes"}
except2 = ["inning","outing","canning","herring","earring","proceed","exceed","succeed"]

# I implement the Porter2 Stemmer following the instruction and phseudo code on the website provide on the lecture slides.


def porter(t):
    if t in except1:
  #      print(f"word {t} is in except1")
        return except1[t]
    wl = list(t)
    r1 = None
    r2 = None
    if wl[0] == 'y':
        wl[0] = 'Y'
    for i in range(0,len(wl) - 1):
        if wl[i] in v and wl[i+1] == 'y':
            wl[i + 1] = 'Y'
    for ex in p_ex:
        if t.find(ex) != -1:
            r1 = t.find(ex) + len(ex)
            break
    for i in range(0,len(wl) - 1):
        if wl[i] in v and wl[i + 1] not in v:
            if (i + 2) <= len(wl) - 1 and r1 == None:
                r1 = i + 2
                break
    if r1 != None:
        for i in range(r1, len(wl) - 1):
            if wl[i] in v and wl[i + 1] not in v:
                if (i + 2) <= len(wl) - 1:
                    r2 = i + 2
                    break
    #print(r1, r2)
    wl = backwardmode(wl, r1, r2)
    #print(f"final: {wl}")
    return "".join(wl)

def backwardmode(wl, r1, r2):
    wl = step1a(wl)
    if "".join(wl) in except2:
   #     print(f"word {wl} is in except 2")
        return "".join(wl)
    wl = step1b(wl,r1)
    wl = step1c(wl)
    wl = step2(wl, r1)
    wl = step3(wl,r1,r2)
    wl = step4(wl,r2)
    wl = step5(wl,r1,r2)
    return wl


def step1a(wl):
    t = "".join(wl)
    t = re.sub("sses$","ss",t)
    if len(t) == 4:
        t = re.sub("(ied|ies)$", "ie", t)
    elif len(t) > 4:
        t = re.sub("(ied|ies)$", "i", t)
    count_v = 0
    for i in t:
        if i in v:
            count_v += 1
    if t[-1] == 's' and len(t) > 1 and ((t[-2] not in v) or count_v >= 2) and (t[-2] != 's'):
        t = t[0:-1]
    #print(f"after 1a: {t}")
    return list(t)

def step1b(wl,r1):
    temp = r1
    if r1 == None:
        temp = len(wl) - 1
    t = "".join(wl)
    pre = t[0:temp]
    region1 = t[temp:]
    region1 = re.sub("(eed|eedly)$","ee",region1)
    t = pre + region1
    count = 0
    for i in t:
        if i in v:
            count += 1
    if count >= 2:
        t = re.sub("(ed|edly|ing|ingly)$","",t)
    if re.search("(at|bl|iz)$",t):
        t = t + "e"
    if len(t) >= 2 and t[-1] in db and t[-1] == t[-2]:
        t = t[0:-1]
    if isShort(t,r1):
        t = t + "e"
    #print(t)
    #print(f"after 1b: {t}")
    return list(t)


def isShort(t,r1):
    if r1 != None:
        return False
    if len(t) == 2 and t[0] in v and t[1] not in v:
        return True
    elif len(t) == 3 and t[-1] not in v_wxy and t[-2] in v and t[-3] not in v:
        return True
    else:
        return False

def step1c(wl):
    if len(wl) > 2 and (wl[-1] == 'y' or wl[-1] == "Y") and wl[-2] not in v:
        wl[-1] = "i"
    #print("".join(wl))
    t = "".join(wl)
    #print(f"after 1c: {t}")
    return wl


def step2(wl,r1):
    if r1 == None:
        return wl
    t = "".join(wl)
    #print(t + " and its r1 index" + str(r1))
    pre = t[0:r1]
    #print("pre: " + pre)
    region1 = t[r1:]
    #print("region1: " + region1)
    region1 = re.sub("tional$", "tion", region1)
    #print("region1: after " + region1)
    region1 = re.sub("enci$", "ence", region1)
    region1 = re.sub("anci$", "ance", region1)
    region1 = re.sub("abli$", "able", region1)
    region1 = re.sub("entli$", "ent", region1)
    region1 = re.sub("izer$", "ization", region1)
    region1 = re.sub("(ational|ation|ator)$", "ate", region1)
    region1 = re.sub("(alism|aliti|alli)$", "al", region1)
    region1 = re.sub("fulness$", "ful", region1)
    region1 = re.sub("(ousli|ousness)$", "ous", region1)
    region1 = re.sub("(iveness|iviti)$", "ive", region1)
    region1 = re.sub("(biliti|bli)$", "ble", region1)
    if re.search("logi$",t):
        region1 = re.sub("ogi$", "og", region1)
    region1 = re.sub("fulli$", "ful", region1)
    region1 = re.sub("lessli$", "less", region1)
    if len(t) >= 3 and t[-3] in valid_LI:
        region1 = re.sub("li$", "", region1)
    t = pre + region1
    #print(t)
    #print(f"word after step2: {t}")
    return list(t)


def step3(wl,r1, r2):
    if r1 == None:
        return wl
    t = "".join(wl)
    pre = t[0:r1]
    #print("pre: " + pre)
    region1 = t[r1:]
    is_r2_modified = False
    region2 = None
    if r2 != None:
        region2 = t[r2:]
    #print("region1: " + region1)
    region1 = re.sub("tional$", "tion", region1)
    #print("region1: after " + region1)
    region1 = re.sub("ational$", "ate", region1)
    region1 = re.sub("alize$", "al", region1)
    region1 = re.sub("(icate|iciti|ical)$", "ic", region1)
    region1 = re.sub("(full|ness)$", "", region1)
    if region2 != None and re.search("ative$",region2):
        region2 = re.sub("ative$","",region2)
        is_r2_modified = True
    if is_r2_modified:
        t = t[0:r2] + region2
    else:
        t = pre + region1
    #print(f"word after step3: {t}")
    return list(t)


def step4(wl,r2):
    if r2 == None:
        return wl
    t = "".join(wl)
    pre = t[0:r2]
    #print("pre: " + pre)
    region2 = t[r2:]
    #print("region1: " + region1)
    region2 = re.sub("(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ism|ate|iti|ous|ive|ize)$", "", region2)
    if len(t) >= 4 and (t[-4] == "s" or t[-4] == "t"):
        region2 = re.sub("ion$", "", region2)
    t = pre + region2
    #print(f"word after step4: {t}")
    return list(t)

def step5(wl,r1,r2):
    if r1 == None:
        return wl
    t = "".join(wl)
    pre = t[0:r1]
    #print("pre: " + pre)
    region1 = t[r1:]
    is_r2_modified = False
    region2 = None
    #print(f"{t} : {r2}")
    if r2 != None:
        region2 = t[r2:]
    if region2 != None and (re.search("e$", region2) or re.search("ll$",region2)):
        region2 = region2[0:-1]
        is_r2_modified = True
    elif len(t) >= 4 and t[-1] == 'e' and  not (t[-2] not in v_wxy and t[-3] in v and t[-4] not in v):
        region1 = region1[0:-1] 
    if is_r2_modified:
        t = t[0:r2] + region2
    else:
        t = pre + region1
    t = t.lower()
    #print(f"word after step5: {t}")
    return list(t)





#porter("sky")
#porter("cries")
#porter("ties")
#porter("tied")
#porter("cats")



