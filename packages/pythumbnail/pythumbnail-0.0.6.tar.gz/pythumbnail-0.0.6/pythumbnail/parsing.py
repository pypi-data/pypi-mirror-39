import re
from .rulegroup import RuleGroup

class Parsing:
    
    def __init__(self, input_s, rulegroup, silence = True):

        self.keys = ['class', 'def', 'for', 'if', 'elif','else:', 'while']
        self.logic = ['in', 'and', 'or', 'not']

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

        FSM_MAP = (
            #  {'src':, 'dst':, 'condition':, 'callback': },
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

        FOR_MAP = (
            #  {'src':, 'dst':, 'condition':, 'callback': },
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
        elif rulegroup.name in['if', 'while']:
            self.map = IFWHILE_MAP
        else:
            self.map = FOR_MAP
        self.current_char = ''
    
    def run(self):
        for i in self.input:
            if not self.process_next(i):
                if not self.silence:
                    print("Skipped")
    
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

    def iterate_re_evaluators(self, achar, transition):
        condition = transition['condition']
        if condition.match(achar):
            self.update_state(transition['dst'], transition['callback'])
            return True
        return False

    def update_state(self, new_state, callback):
        if not self.silence:
            print("{} -> {} : {}".format(self.current_char, self.state, new_state))
        self.state = new_state
        callback(self)


def T_APPEND_NAME(fsm_obj):
    fsm_obj.rulegroup.functionname += fsm_obj.current_char

def T_APPEND_NEW_NAME(fsm_obj):
    fsm_obj.rulegroup.functionname += ' and '
    
def T_ADDLOGIC(fsm_obj):
    fsm_obj.rulegroup.logic[fsm_obj.rulegroup.num_logic] += fsm_obj.current_char
    
def T_NEWLOGIC(fsm_obj):
    fsm_obj.rulegroup.num_logic += 1
    fsm_obj.rulegroup.logic.append('')
    if fsm_obj.current_char != ' ':
        fsm_obj.rulegroup.logic[fsm_obj.rulegroup.num_logic] += fsm_obj.current_char
    
def T_TRANSIT(fsm_obj):
    pass

def T_ADDPARA(fsm_obj):
    fsm_obj.rulegroup.params[fsm_obj.parameter] += fsm_obj.current_char
    
def T_NEWPARA(fsm_obj):
    fsm_obj.rulegroup.params.append('')
    fsm_obj.parameter += 1
    if fsm_obj.current_char != ' ':
        fsm_obj.rulegroup.params[fsm_obj.parameter] += fsm_obj.current_char