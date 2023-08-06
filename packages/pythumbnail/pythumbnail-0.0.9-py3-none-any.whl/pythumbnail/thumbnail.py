"""
Thumbnail Class
=============

Thumbnail class in pythumbnail handles higher level parsing as it tracks 
the relationship between different function groups (For example, if the 
function belongs to a class or if the for loop is nested under another 
for loop) with indentation. It also provides functions such as search and 
show_summary that allows users to get more specific information

"""

import re
from .rulegroup import RuleGroup
from .parsing import Parsing

class thumbnail:

    """
    A class for high level parsing

    Attributes:
    ----------

    filename: string
        name of the file
    data: list
        A list of strings containing the content of input python file
    summary: dict
        A dictionary counting the number of occurrence of each function group
    tree: RuleGroup
        Root node of the parsed tree
    keys: list
        A list of strings including the keywords of function groups
    print_keys: list
        User applied filter on the keywords visible (default = keys)
    silence: boolean
        if set to true, output logging


    Methods:
    --------
    
    __detect_group(string, group_level)
        detect whether the first word in the string is within dictionary

    __check_group_level(string, group_level)
        return the number of indentation in the string

    scan()
        iterate through the entire document and return the complete parsing tree

    search(name, start=None)
        return the node with functionname equals name

    show_summary()
        return the summary dictionary

    show_text()
        return the data list

    """

    def __init__(self, directory, silence, keys):

        self.filename = directory.split('/')[-1]

        if self.filename == '' or self.filename.split('.')[1] != 'py':
            raise "Input is not Python file"

        with open (directory, "r") as myfile:
            self.data = myfile.readlines()

        self.summary = None
        self.tree = RuleGroup(None, 'File', -1, True) # set the filename as root node
        self.keys = ['class', 'def', 'for', 'if', 'elif', 'else:', 'while']
        self.print_keys = keys
        self.silence = silence

    # detect whether the first word in the string is within dictionary
    def __detect_group(self, string, group_level):
        k = string[group_level:].split()
        if not len(k) == 0 and k[0] in self.keys:
            return k[0]
        else:
            return None

    # check the indentation of the string
    def __check_group_level(self, string):
        level = 0 
        while level < len(string) and string[level] == ' ' or string[level] == '\t':
            level += 1
        return level

    # scan through entire document
    def scan(self):

        # initialization
        group_level = 0
        self.tree = RuleGroup(None, 'File', -1, True)
        self.tree.functionname = self.filename
        self.summary = {'class': 0, 'def': 0, 'for': 0, 'if': 0, 'while': 0}
        
        group_parent = [(-1, self.tree)]
        token_tree = []
        
        # go through every row
        for i in self.data:
            
            # skip if the line is empty
            if i == '\n':
                continue
            
            # get new indentation level
            group_level = self.__check_group_level(i)
            
            # adjust the list of parents
            for t in range(len(group_parent)):
                if group_parent[t][0] >= group_level:
                    group_parent = group_parent[:t]
                    break
            
            # detect keyword in the string
            check = self.__detect_group(i, group_level)
            
            if not check is None:
                
                if check in self.summary:
                    self.summary[check] += 1
                
                r = RuleGroup(group_parent[-1], check, group_level, check in self.print_keys)
                p = Parsing(i[group_level + len(check) + 1:], r, self.silence)
                p.run()
                token_tree.append(r)
                group_parent.append((group_level, r))
                
                group_parent[-2][1].child.append(r)

    # search for a node using its function name
    def search(self, name, start = None):

        if start is None:
            start = self.tree

        result = None

        for i in start.child:
            if i.functionname == name:
                return i
            result = self.search(name, start = i)

        return result

    # output a brief summary of the string
    def show_summary(self):
        if self.summary is None:
            raise("Run scan function first to get summary information")
        for i in self.summary:
            print(i, ': ', self.summary[i])
        return self.summary

    # return the entire text file as array
    def show_text(self):
        return self.data
