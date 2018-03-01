import os
from graphviz import Digraph

PATH='C:/Users/njoy/Workspace/Maggi/Assets/Scripts/Game/EventsV2/EventV2Types/LeaderboardEventV2'

first_adj = ["public", "protected", "private"]
variable_type = ["int", "bool", "long", "float"]


def getAllVariables(line, filename):
    if line.endswith(";") and "using" not in line:
        split_line = line.split(' ')
        if split_line[0] in first_adj and split_line[1] in variable_type or split_line[0] in variable_type:
            print(filename + " " + line)

def getAllObjects(line):
    split_line = line.split(' ')
    if split_line[0] in first_adj and (split_line[1] == "class" or split_line[1] == "enum"):
        variable_type.append(split_line[2])
    else:
        return
    
for dirname, dirnames, filenames in os.walk(PATH):

    # print path to all filenames.
    for filename in filenames:
        if not filename.endswith('.meta'):
            path = os.path.join(dirname, filename) 
            f = open(path, 'r')
            while True:
                c = f.readlines(1)
                if not c:
                    break
                c = [x.strip() for x in c]
                for line in c:
                    getAllObjects(line)
            f = open(path, 'r')
            while True:
                c = f.readlines(1)
                if not c:
                    break
                c = [x.strip() for x in c]
                for line in c:
                    getAllVariables(line, filename)
                    
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')
        
