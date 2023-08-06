class RuleGroup:
    def __init__(self, parent, name, group_level, visible):
        self.parent = parent
        self.child = []
        self.name = name
        self.functionname = ''
        self.params = ['']
        self.logic = []
        self.num_logic = -1
        self.group_level = group_level
        self.visible = visible
    
    def __str__(self, level=0):
        if self.visible:
            if self.name == 'for':
                ret = "\t"*level+repr(self.name + ' ' + self.functionname + ' ' + self.logic[0] + ','.join(self.params))+"\n"
            elif self.name == 'if' or self.name == 'while':
                ret = "\t"*level+repr(self.name + '[' + ','.join(self.params) + '] LOGIC: ['+ ','.join(self.logic) + ']') +"\n"
            else:
                ret = "\t"*level+repr(self.name + ' ' + self.functionname + '(' + ','.join(self.params) + ')')+"\n"
            for c in self.child:
                ret += c.__str__(level+1)
        else:
            ret = ""
            for c in self.child:
                ret += c.__str__(level)
        return ret

    def __repr__(self):
        return '<tree node representation>'