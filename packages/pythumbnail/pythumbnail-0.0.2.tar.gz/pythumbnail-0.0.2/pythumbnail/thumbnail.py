import re
from .rulegroup import RuleGroup
from .parsing import Parsing

class thumbnail:

    def __init__(self, directory, silence = True, tab_to_space = 4):

        self.filename = directory.split('/')[-1]

        if self.filename == '':
            raise "Please input directory in the correct format"

        with open (directory, "r") as myfile:
            self.data = myfile.readlines()

        self.tab_to_space = tab_to_space
        self.summary = None
        self.tree = RuleGroup(None, 'File', -1)
        self.keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']
        self.silence = silence

    def __detect_group(self, string, group_level):
        k = string[group_level:].split()
        if not len(k) == 0 and k[0] in self.keys:
            return k[0]
        else:
            return None

    def __check_group_level(self, string):
        level = 0 
        tab_level = 0 
        while level < len(string) and string[level] == ' ' or string[level] == '\t':
            if string[level] == '\t':
                tab_level += 1
            level += 1
        return level + (self.tab_to_space - 1) * tab_level

    def scan(self):
        group_level = 0
        self.tree = RuleGroup(None, 'File', -1)
        self.tree.functionname = self.filename
        self.summary = {'class': 0, 'def': 0, 'for': 0, 'if': 0, 'while': 0}
        
        group_parent = [(-1, self.tree)]
        token_tree = []
        
        for i in self.data:
            
            if i == '\n':
                continue
            
            group_level = self.__check_group_level(i)
            
            for t in range(len(group_parent)):
                if group_parent[t][0] >= group_level:
                    group_parent = group_parent[:t]
                    break
                    
            check = self.__detect_group(i, group_level)
            
            if not check is None:
                
                if check in self.summary:
                    self.summary[check] += 1
                
                r = RuleGroup(group_parent[-1], check, group_level)
                p = Parsing(i[group_level + len(check) + 1:], r, self.silence)
                p.run()
                token_tree.append(r)
                group_parent.append((group_level, r))
                
                group_parent[-2][1].child.append(r)

    def show_summary(self):
        if self.summary is None:
            raise("Run scan function first to get summary information")
        for i in self.summary:
            print(i, ': ', self.summary[i])
        return self.summary
