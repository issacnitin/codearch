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

class ClassStructure:
    def __init__(self, members, functions):
        self.members = members
        self.functions = functions
