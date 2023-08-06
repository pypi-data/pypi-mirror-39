"""
RuleGroup Class
=============

RuleGroup class in pythumbnail represents each node in the parsing tree. 
It contains information about the node (name, functionname, logic...) 
as well as its successor and predecessor.

"""

class RuleGroup:

    """
    A class representing a single node in parsing tree

    Attributes:
    ----------

    parent: RuleGroup
        predecessor
    child: list
        successors
    name: string
        function group category (e.g. def)
    functionname: string
        name of the function group
    params: list
        list of parameters
    logic: list
        list of logical operators
    num_logic: int
        number of logical operators - 1
    group_level: int
        number of indentations
    visible: boolean
        If True, the node will be printed in the tree

    
    Methods:
    --------

    __str__(level=0)
        print out the information about the node and its children recursively

    __repr__()
        define string reputation of the class

    """

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
    
    # print out the node tree
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
        return '<pythumbnail node>: ' + self.functionname