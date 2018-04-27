import os
import re
from graphviz import Digraph

PATH='/Users/nitinissacjoy/OpenSource/AngryBirdsStyleGame/Assets/Scripts/test'

first_adj = ["public", "protected", "private"]
second_adj = ["static", "const"]
garbage = first_adj + second_adj
garbage += ['', 'if', 'else', '(', ')', '=', '==', '<', '>', '&', '&&', '|', '||', '.', 'get', 'set', 'new', 'return', 'yield', '{', '}', 'IEnumerator']
dot = Digraph(comment="Variable Generation from code")

dict = {}

def getAllVariables(line, filename):
    if "using" not in line:
        split_line = line.split(' |=')
        if split_line[0] in first_adj and split_line[1] not in second_adj:
            dict[filename]['variables'].append(split_line[1])
        #    dot.node(split_line[2])
        #    dot.edge(filename, split_line[2], constraint='false')
        elif split_line[0] in first_adj and split_line[1] in second_adj:
            dict[filename]['variables'].append(split_line[2])
        #    print(filename + " " + split_line[1])
        #    dot.node(split_line[1])
        #    dot.edge(filename, split_line[1], constraint='false')
        # else:
        #   dict[filename]['variables'].append(split_line[0])
            
def getAllObjects(filename, line):
    split_line = line.split(' ')
    if split_line[0] in first_adj and (split_line[1] == "class" or split_line[1] == "enum"):
        dict[filename]['class'].append(split_line[2])
    else:
        return
    
for dirname, dirnames, filenames in os.walk(PATH):
    # print path to all filenames.
    for filename in filenames:
        dict[filename] = {}
        dict[filename]['class'] = []
        dict[filename]['variables'] = []
        dict[filename]['using'] = []
        dict[filename]['enum'] = []
        dict[filename]['functions'] = []
        dict[filename]['access'] = []
        if filename.endswith('.cs'):
            st = []
            path = os.path.join(dirname, filename) 
            f = open(path, 'r')
            lines = f.read().decode("utf-8-sig").encode("utf-8").split('\n')
            for key in lines:
                if key.find("//") != -1:
                    key = key[:key.find("//")]
                if key.find('using') != -1:
                    _key = key.split(' ')
                    dict[filename]['using'].append(_key[_key.index('using')+1])
                elif key.find('class') != -1:
                    _key = key.split(' ')
                    dict[filename]['class'].append(_key[_key.index('class')+1])
                elif key.find('enum') != -1: #elif is dangerous
                    _key = key.split(' ')
                    dict[filename]['enum'].append(_key[_key.index('enum')+1])
                elif re.search(r'<.*>', key):
                    dict[filename]['access'].append(key[re.search(r'<', key).start()+1:re.search(r'>', key).start()])
                elif re.search(r'\(.*\)', key):
                    _key = key.split('(')
                    _key = _key[0].split(' ')
                    for word in _key:
                        if word not in garbage:
                            dict[filename]['functions'].append(word)
                            break
                else:
                    _key = key.split(' ')
                    skip = False
                    for i,word in enumerate(_key):
                        if skip:
                            skip = False
                            continue
                        if word not in garbage and word[:-1] not in garbage and i+1 < len(_key) and _key[i+1] not in garbage:
                            if not i+1 < len(_key):
                                continue
                            dict[filename]['variables'].append({
                                "type": word,
                                "name": _key[i+1]
                            })
                            skip = True
                        
            # while True:
            #     c = f.readlines(1)
            #     if not c:
            #         break
            #     c = [x.strip() for x in c]
            #     for line in c:
            #         getAllObjects(filename, line)
            # f = open(path, 'r')
            # while True:
            #     c = f.readlines(1)
            #     if not c:
            #         break
            #     c = [x.strip() for x in c]
            #     for line in c:
            #         getAllVariables(line, filename) 
    for file in dict:
        for key in dict[file]:
            print(key + " " + str(dict[file][key]) + "\n")             
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')
        
