import os
import re
import helper, json
from graphviz import Digraph
from subprocess import Popen, PIPE
from cStringIO import StringIO

PATH='/Users/nitinissacjoy/Workspace/Socket'
LANGUAGE="C++"
SKIP_DIR=['.git']

dot = Digraph(comment="Variable Generation from code")

# Step 1: Get all keywords for language
f = open("./language_spec/" + LANGUAGE + ".ca", "r+")
json_config = f.read()
language_spec = json.loads(json_config)
keywords = language_spec["KEYWORDS"]
code_block_start = language_spec["BRACKET"]["block"]["start"]
code_block_end = language_spec["BRACKET"]["block"]["end"]

class_keywords = language_spec["CLASS"]

# Step 2: Get all classnames from codebase
# Need to redo weeding out comment blocks
class_names = []
class_meta = {}
for dir_name, dir_names, file_names in os.walk(PATH):
    skip = False
    for name in SKIP_DIR:
        if name in dir_name:
            skip = True
            break
    if skip:
        continue
    for file_name in file_names:
        path = os.path.join(dir_name, file_name)
        f = open(path, "r+")
        source_code = f.read()
        _input = StringIO(source_code)
        _output = StringIO()

        process = Popen(['sed', '', 'language_spec/C++.sed', path], stdout=PIPE, stderr=PIPE)
        stripped_code, stderr = process.communicate()
        lines = stripped_code.split('\n')
        
        line_count = -1
        for key in lines:
            line_count += 1
            words = key.split(' ')
            for class_keyword in class_keywords:
                if class_keyword in words:
                    try:
                        if words[words.index(class_keyword) + 1] not in class_names:
                            class_names.append(re.split('(\W)', words[words.index(class_keyword)+1])[0])
                            class_meta[re.split('(\W)', words[words.index(class_keyword)+1])[0]] = {
                                'file_path': path,
                                'line': line_count
                            }
                    except:
                        print("Some error occured somewhere")
class_link = {}
st = []
for key in class_meta:
    f = open(class_meta[key]['file_path'], "r+")
    source_code = f.read()
    input = StringIO(source_code)
    output = StringIO()

    process = Popen(['sed', '', 'language_spec/C++.sed', path], stdout=PIPE, stderr=PIPE)
    stripped_code, stderr = process.communicate()
    lines = stripped_code.split('\n')
 
    line_count = -1
    class_link[key] = []
    for line in lines:
        line_count += 1
        if line_count >= class_meta[key]['line']:
            words = re.split('(\W)', line)
            for word in words:
                if word == code_block_start:
                    st.append(word)
                if len(st) > 0 and word == code_block_end:
                    st.pop()
                if len(st) == 1: #highest block in class structure, not inner blocks
                    if word in class_names:
                        if word not in class_link[key]:
                            class_link[key].append(word)

for key in class_link:
    if key == "":
        continue
    dot.node(key)
    for node in class_link[key]:
        if node == "":
            continue
        dot.edge(key, node)
dot.render('code-graph', view=True)  
# dict = {}    
# for dirname, dirnames, filenames in os.walk(PATH):
#     # print path to all filenames.
#     for filename in filenames:
#         dict[filename] = {}
#         dict[filename]['class'] = []
#         dict[filename]['variables'] = []
#         dict[filename]['using'] = []
#         dict[filename]['enum'] = []
#         dict[filename]['functions'] = []
#         dict[filename]['access'] = []
#         if filename.endswith('.cs'):
#             st = []
#             path = os.path.join(dirname, filename) 
#             f = open(path, 'r')
#             lines = f.read().decode("utf-8-sig").encode("utf-8").split('\n')
#             for key in lines:
#                 if key.find("//") != -1:
#                     key = key[:key.find("//")]
#                 if key.find('using') != -1:
#                     _key = key.split(' ')
#                     dict[filename]['using'].append(_key[_key.index('using')+1])
#                 elif key.find('class') != -1:
#                     _key = key.split(' ')
#                     dict[filename]['class'].append(_key[_key.index('class')+1])
#                 elif key.find('enum') != -1: #elif is dangerous
#                     _key = key.split(' ')
#                     dict[filename]['enum'].append(_key[_key.index('enum')+1])
#                 elif re.search(r'<.*>', key):
#                     dict[filename]['access'].append(key[re.search(r'<', key).start()+1:re.search(r'>', key).start()])
#                 elif re.search(r'\(.*\)', key):
#                     _key = key.split('(')
#                     _key = _key[0].split(' ')
#                     for word in _key:
#                         if word not in garbage:
#                             dict[filename]['functions'].append(word)
#                             break
#                 else:
#                     _key = key.split(' ')
#                     skip = False
#                     for i,word in enumerate(_key):
#                         if skip:
#                             skip = False
#                             continue
#                         if word not in garbage and word[:-1] not in garbage and i+1 < len(_key) and _key[i+1] not in garbage:
#                             if not i+1 < len(_key):
#                                 continue
#                             dict[filename]['variables'].append({
#                                 "type": word,
#                                 "name": _key[i+1]
#                             })
#                             skip = True
                        
#             # while True:
#             #     c = f.readlines(1)
#             #     if not c:
#             #         break
#             #     c = [x.strip() for x in c]
#             #     for line in c:
#             #         getAllObjects(filename, line)
#             # f = open(path, 'r')
#             # while True:
#             #     c = f.readlines(1)
#             #     if not c:
#             #         break
#             #     c = [x.strip() for x in c]
#             #     for line in c:
#             #         getAllVariables(line, filename) 
#     for file in dict:
#         for key in dict[file]:
#             print(key + " " + str(dict[file][key]) + "\n")             
#     # Advanced usage:
#     # editing the 'dirnames' list will stop os.walk() from recursing into there.
#     if '.git' in dirnames:
#         # don't go into any .git directories.
#         dirnames.remove('.git')
        
