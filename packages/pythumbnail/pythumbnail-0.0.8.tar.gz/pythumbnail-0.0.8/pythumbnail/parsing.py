"""
Parsing Class
=============

Parsing class in pythumbnail uses finite state machine (FSM)
to further break down the input into multiple key parts including
name of the function, parameters and logical relationship between 
parameters (==/</>) if the input is if or while statement

"""


import re
from .rulegroup import RuleGroup

class Parsing:

    """
    A class for further parsing information in each line

    Attributes:
    ----------

    (FSM States)
    S_NAME: defining name of the function
    S_STRING: inputing information into a string (spaces do not cause state changes)
    S_PARA: defining parameters of the function
    S_COMMA: adding new parameters
    S_LOGIC: defining logical relationships
    S_END_RULE: end of sentences
    
    (Other variables)
    input: string
        the input string
    state: string
        current stage 
    parameter: int
        number of parameters
    rulegroup: rulegroup
        object that carries information about the input
    silence: boolean
        if set to true, output logging
    map: dict
        dictionary including all the rules for parsing
    current_char: string
        current character being processed

    
    Methods:
    -------

    run()
        iterate through each character in the input string

    process_next(achar)
        check the current state. Exit if the state is S_END_RULE

    iterate_re_evaluators(achar, transition)
        evaluate if the given conditions match any case defined in FSM map

    update_case(new_state, callback)
        call the transition function and update current state according to rules defined in map

    """
    def __init__(self, input_s, rulegroup, silence = True):

        # define keyword libraries
        self.logic = ['in', 'and', 'or', 'not']

        # define the states in finite state machine
        self.S_NAME = "STATE: NAME"
        self.S_STRING = "STATE: STRING"
        self.S_PARA = "STATE: DEFINE PARAMETERS"
        self.S_COMMA = "STATE: NEW PARAMETERS"
        self.S_LOGIC = "STATE: LOGICAL OPERATORS"
        self.S_END_RULE = "STATE: END RULE"

        self.input = input_s
        self.state = self.S_NAME
        self.parameter = 0
        self.rulegroup = rulegroup
        self.silence = silence

        # FSM (Finite State Machine) map for functions (def)
        FSM_MAP = (
            {'src': self.S_NAME,
             'dst': self.S_NAME,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|'|\d]"),
             'callback': T_APPEND_NAME},
            {'src': self.S_NAME,
             'dst': self.S_PARA,
             'condition': re.compile("\("),
             'callback': T_TRANSIT},
            {'src': self.S_PARA,
             'dst': self.S_PARA,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|'|\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_PARA,
             'dst': self.S_COMMA,
             'condition': re.compile("\,"),
             'callback': T_NEWPARA},
            {'src': self.S_COMMA,
             'dst': self.S_PARA,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|'|\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_PARA,
             'dst': self.S_END_RULE,
             'condition': re.compile("\)"),
             'callback': T_TRANSIT},
            {'src': self.S_COMMA,
             'dst': self.S_END_RULE,
             'condition': re.compile("\)"),
             'callback': T_TRANSIT}
        )

        # FSM map for for loops (for)
        FOR_MAP = (
            {'src': self.S_NAME,
             'dst': self.S_NAME,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|(|\)|\d]"),
             'callback': T_APPEND_NAME},
            {'src': self.S_NAME,
             'dst': self.S_STRING,
             'condition': re.compile("\"|\'"),
             'callback': T_APPEND_NAME},
            {'src': self.S_STRING,
             'dst': self.S_STRING,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|(|\)| |\d]"),
             'callback': T_APPEND_NAME},
            {'src': self.S_STRING,
             'dst': self.S_NAME,
             'condition': re.compile("\"|\'"),
             'callback': T_APPEND_NAME},
            {'src': self.S_NAME,
             'dst': self.S_COMMA,
             'condition': re.compile("\,"),
             'callback': T_APPEND_NEW_NAME},
            {'src': self.S_COMMA,
             'dst': self.S_COMMA,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|(|\)|'|\d]"),
             'callback': T_APPEND_NAME},
            {'src': self.S_COMMA,
             'dst': self.S_NAME,
             'condition': re.compile("\,"),
             'callback': T_APPEND_NEW_NAME},
            {'src': self.S_NAME,
             'dst': self.S_LOGIC,
             'condition': re.compile("\ "),
             'callback': T_NEWLOGIC},
            {'src': self.S_COMMA,
             'dst': self.S_LOGIC,
             'condition': re.compile("\ "),
             'callback': T_NEWLOGIC},
            {'src': self.S_LOGIC,
             'dst': self.S_LOGIC,
             'condition': re.compile("[A-Za-z]"),
             'callback': T_ADDLOGIC},
            {'src': self.S_LOGIC,
             'dst': self.S_PARA,
             'condition': re.compile("\ "),
             'callback': T_ADDPARA},
            {'src': self.S_PARA,
             'dst': self.S_PARA,
             'condition': re.compile("[A-Za-z|+|-|_|,|.|[|\]|(|\)|'|\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_PARA,
             'dst': self.S_END_RULE,
             'condition': re.compile("\:"),
             'callback': T_TRANSIT}
        )

        # FSM map for if and while statements
        IFWHILE_MAP = (
            {'src': self.S_NAME,
             'dst': self.S_NAME,
             'condition': re.compile("[A-Za-z|+|-|_|,|.|[|\]|(|\)|\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_NAME,
             'dst': self.S_STRING,
             'condition': re.compile("\"|\'"),
             'callback': T_ADDPARA},
            {'src': self.S_STRING,
             'dst': self.S_STRING,
             'condition': re.compile("[A-Za-z|+|-|_|[|\]|(|\)| |\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_STRING,
             'dst': self.S_NAME,
             'condition': re.compile("\"|\'"),
             'callback': T_ADDPARA},
            {'src': self.S_NAME,
             'dst': self.S_END_RULE,
             'condition': re.compile("\:"),
             'callback': T_TRANSIT},
            {'src': self.S_NAME,
             'dst': self.S_LOGIC,
             'condition': re.compile("[<|>|=| |]"),
             'callback': T_NEWLOGIC},
            {'src': self.S_LOGIC,
             'dst': self.S_LOGIC,
             'condition': re.compile("[=|<|>|]"),
             'callback': T_ADDLOGIC},
            {'src': self.S_LOGIC,
             'dst': self.S_PARA,
             'condition': re.compile("[A-Za-z| |]"),
             'callback': T_NEWPARA},
            {'src': self.S_PARA,
             'dst': self.S_PARA,
             'condition': re.compile("[A-Za-z|+|-|_|,|.|[|\]|(|\)|'|\d]"),
             'callback': T_ADDPARA},
            {'src': self.S_PARA,
             'dst': self.S_LOGIC,
             'condition': re.compile("\ "),
             'callback': T_NEWLOGIC},
            {'src': self.S_PARA,
             'dst': self.S_END_RULE,
             'condition': re.compile("\:"),
             'callback': T_TRANSIT},
        )

        if rulegroup.name in ['class', 'def']:
            self.map = FSM_MAP
        elif rulegroup.name in ['if', 'while']:
            self.map = IFWHILE_MAP
        else:
            self.map = FOR_MAP
        self.current_char = ''
    
    # go through all elements in the string
    def run(self):
        for i in self.input:
            if not self.process_next(i):
                if not self.silence:
                    print("Skipped")

    # process each individal character
    def process_next(self, achar):
        self.current_char = achar
        state = self.state
        
        if state == self.S_END_RULE:
            return True
        
        for transition in self.map:
            if transition['src'] == state:
                if self.iterate_re_evaluators(achar, transition):
                    return True
        return False

    # evaluate whether the character evokes state change
    def iterate_re_evaluators(self, achar, transition):
        condition = transition['condition']
        if condition.match(achar):
            self.update_state(transition['dst'], transition['callback'])
            return True
        return False

    # print out state update
    def update_state(self, new_state, callback):
        if not self.silence:
            print("{} -> {} : {}".format(self.current_char, self.state, new_state))
        self.state = new_state
        callback(self)

"""

FSM Transitions:
----------------

T_APPEND_NAME(fsm_obj):
    append the current character to functionname string

T_APPEND_NEW_NAME(fsm_obj):
    create an empty new functionname and concatenate it with the functionname string using 'and'

T_ADDLOGIC(fsm_obj):
    append the current character to logic string

T_NEWLOGIC(fsm_obj):
    create a new logic string

T_TRANSIT(fsm_obj):
    no transition function (pass)

T_ADDPARA(fsm_obj):
    append the current character to parameter string

T_NEWPARA(fsm_obj):
    create a new parameter string

"""

def T_APPEND_NAME(fsm_obj):
    fsm_obj.rulegroup.functionname += fsm_obj.current_char

def T_APPEND_NEW_NAME(fsm_obj):
    fsm_obj.rulegroup.functionname += ' and '
    
def T_ADDLOGIC(fsm_obj):
    fsm_obj.rulegroup.logic[fsm_obj.rulegroup.num_logic] += fsm_obj.current_char
    
def T_NEWLOGIC(fsm_obj):
    fsm_obj.rulegroup.num_logic += 1
    fsm_obj.rulegroup.logic.append('')
    # skip appending if the character is space
    if fsm_obj.current_char != ' ':
        fsm_obj.rulegroup.logic[fsm_obj.rulegroup.num_logic] += fsm_obj.current_char
    
def T_TRANSIT(fsm_obj):
    pass

def T_ADDPARA(fsm_obj):
    fsm_obj.rulegroup.params[fsm_obj.parameter] += fsm_obj.current_char
    
def T_NEWPARA(fsm_obj):
    fsm_obj.rulegroup.params.append('')
    fsm_obj.parameter += 1
    # skip appending if the character is space
    if fsm_obj.current_char != ' ':
        fsm_obj.rulegroup.params[fsm_obj.parameter] += fsm_obj.current_char