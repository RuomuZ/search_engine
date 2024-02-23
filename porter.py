import re

v = ['a','e','i','o','u']
v_wxy = ['a','e','i','o','u','x','Y','z']
valid_LI = ['c','d','e','g','h','k','m','n','r','t']
p_ex = ['gener','commun','arsen']



def porter(t):
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


def backwardmode(wl, r1, r2):
    wl = step1a(wl)
    wl = step1b(wl,r1)
    wl = step1c(wl)

def step1a(wl):
    t = "".join(wl)
    t = re.sub("sses$","ss",t)
    if len(t) == 4:
        t = re.sub("(ied|ies)$", "ie", t)
    elif len(t) > 4:
        t = re.sub("(ied|ies)$", "i", t)
    if t[-1] == 's' and len(t) > 1 and (t[-2] not in v) and (t[-2] != 's'):
        t = t[0:-1]
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
    if len(t) >= 2 and t[-1] not in v and t[-1] == t[-2]:
        t = t[0:-1]
    if isShort(t,r1):
        t = t + "e"
    #print(t)
    return list(t)


def isShort(t,r1):
    if r1 != None:
        return False
    if len(t) == 2 and t[0] in v and t[1] not in v:
        return True
    elif len(t) > 2 and t[-1] not in v_wxy and t[-2] in v and t[-3] not in v:
        return True
    else:
        return False

def step1c(wl):
    if len(wl) > 2 and (wl[-1] == 'y' or wl[-1] == "Y") and wl[-2] not in v:
        wl[-1] = "i"
    print("".join(wl))
    return wl

porter("by")
#porter("cries")
#porter("ties")
#porter("tied")
#porter("cats")



