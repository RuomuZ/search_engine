import os
from bs4 import BeautifulSoup
import json
import re
import porter
from urllib.parse import urlparse



def get_files():
    file_list = []
    l = os.listdir("DEV")
    for i in l:
        k = os.listdir("DEV/" + i) 
        for f in k:
            file_list.append("DEV/" + i + "/" + f)
    return file_list

def get_batch(fl):
    toReturn = []
    batch = []
    counter_1 = len(fl)
    counter_2 = 0
    while counter_1 > 0:
        counter_1 -= 1
        batch.append(fl[counter_1])
        counter_2 += 1
        if counter_2 == 2500 or counter_1 == 0:
            toReturn.append(batch)
            batch = []
            counter_2 = 0
    return toReturn
        
def get_aggre_batch(fl):    
    toReturn = []
    batch = []
    counter_1 = len(fl)
    counter_2 = 0
    while counter_1 > 0:
        counter_1 -= 1
        batch.append(fl[counter_1])
        counter_2 += 1
        if counter_2 == 10 or counter_1 == 0:
            toReturn.append(batch)
            batch = []
            counter_2 = 0
    return toReturn



def get_content(f_name):
    f = open(f_name,"r")
    toReturn = json.load(f)
    f.close()
    return toReturn

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif re.match(
                r".*\.(ff|css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1|rar|doc|sql|lua|h|c|sr"
                + r"|thmx|mso|arff|rtf|jar|md|csv|@uci.edu|@ics.uci.edu"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|jpg|java|py|ppsx|scm)$",
                parsed.path.lower()):
            return False 
        elif re.match(
                r".*\.(ff|css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1|rar|doc|sql|lua|h|c|sr"
                + r"|thmx|mso|arff|rtf|jar|md|csv|@uci.edu|@ics.uci.edu"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|jpg|java|py|ppsx|scm)$",
                parsed.query.lower()):
            return False
        else:
            return True
    except TypeError:
        print("TypeError for ", parsed)
        raise

        


def map_f():
    fl = get_files()
    total_f = len(fl)
    fl = get_batch(fl)
    page_indexed = 0
    doc_dict = {}
    inverted = {}
    counter = 0
    word_set = set()
    for c in range(0,len(fl)):
        for f in fl[c]:
            print(str(counter) + " : " + f)
            content = get_content(f)
            if not is_valid_url(content["url"]):
                counter += 1
                total_f -= 1
                continue
            doc_dict[str(counter)] = content["url"]
            soup = BeautifulSoup(content["content"],"html.parser")        
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text().lower()
            myP = r"[a-z0-9]{2,23}"
            target_list = re.findall(myP,text)
            count = len(target_list)
            for i in range(0,count):
                t = porter.porter(target_list[i])
                word_set.add(t)
                if t not in inverted:
                    inverted[t] = {}
                    inverted[t][str(counter)] = [[i],count]
                elif str(counter) not in inverted[t]:
                    inverted[t][str(counter)] = [[i],count]
                else:
                    inverted[t][str(counter)][0].append(i)
            counter += 1
        keys = inverted.keys()
        #print(keys) 
        for key in keys:
        #v -> [[positions],count]
            new_v = []
            for post in inverted[key].items():
                doc_id, v = post
                new = (doc_id, v[0], int((len(v[0])/v[1]) * 10000))
                new_v.append(new)
            inverted[key] = new_v
        with open(f"map/batch_{c}.json", "w") as f:
            json.dump(inverted, f)
        inverted.clear()
    with open(f"url_id_match.json", "w") as f:
        json.dump(doc_dict, f)
    print(total_f)
    return word_set


def aggre():
    file_list = []
    k = os.listdir("map")
    for f in k:
        file_list.append("map/" + f)
    batch_list = get_aggre_batch(file_list)
    counter = 0
    for batch in batch_list:
        inverted = {}
        for f in batch:
            inde = get_content(f)
            keys = inde.keys()
            for key in keys:
                if key in inverted:
                    inverted[key].extend(inde[key])
                else:
                    inverted[key] = inde[key] 
        with open(f"reduce/agg_{counter}.json", "w") as f:
            json.dump(inverted, f)
        counter += 1
    
def finalize(word_set):
    l = list(word_set) 
    word_c = [[],[],[]]
    for w in l:
        if len(w) < 5:
            word_c[0].append(w)
        elif len(w) >= 5 and len(w) < 12:
            word_c[1].append(w)
        else:
            word_c[2].append(w)
    file_list = []
    k = os.listdir("reduce")
    for f in k:
        file_list.append("reduce/" + f)
    counter = 0
    for c in word_c:
        c = set(c)
        inverted = {}
        for f in file_list: 
            inde = get_content(f)
            keys = inde.keys()
            for key in keys:
                if key in c and key in inverted:
                    inverted[key].extend(inde[key])
                elif key in c:
                    inverted[key] = inde[key] 
        with open(f"index_{counter}.json", "w") as f:
            json.dump(inverted, f)
        counter += 1
    
if __name__ == "__main__":
    word_set = map_f()
    aggre()
    finalize(word_set)
    print(len(word_set))
