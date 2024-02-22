import re

v = ['a','e','i','o','u']
v_wxy = ['a','e','i','o','u','x','y','z']
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
    for i in range(r1, len(wl) - 1):
        if wl[i] in v and wl[i + 1] not in v:
            if (i + 2) <= len(wl) - 1:
                r2 = i + 2
                break
    print(r1, r2)

porter("generation")
        


