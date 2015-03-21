# ------------------------------------------------------------
# lexer.py
#
# tokenizer for TinyC
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
symbols = [
   'RBRACE',
   'SEMICOLON',
   'TIMES',
   'NOT',
   'LPAR',
   'LBRACK',
   'COMMA',
   'DIVIDE',
   'RPAR',
   'RBRACK',
   'PLUS',
   'EQUAL',
   'GREATER',
   'NEQUAL',
   'LBRACE',
   'ASSIGN',
   'MINUS',
   'LESS',
   'KEYWORD',
]

other = [
   'NAME',
   'NUMBER',
   'QCHAR',
   ]

reserved = { 
   'int'    :   'INT',
   'return' :   'RETURN',
   'else'   :   'ELSE',
   'char'   :   'CHAR',
   'while'  :   'WHILE',
   'write'  :   'WRITE',
   'if'     :   'IF',
   'read'   :   'READ',
   'length' :   'LENGTH',
}

tokens = symbols + other + reserved.values()

# Regular expression rules for simple tokens
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_TIMES     = r'\*'
t_NOT       = r'!'
t_LPAR      = r'\('
t_LBRACK    = r'\['
t_COMMA     = r','
t_DIVIDE    = r'/'
t_RPAR      = r'\)'
t_RBRACK    = r'\]'
t_PLUS      = r'\+'
t_EQUAL     = r'=='
t_GREATER   = r'>'
t_NEQUAL    = r'!='
t_LBRACE    = r'\{'
t_ASSIGN    = r'='
t_MINUS     = r'\-'
t_LESS      = r'<'
t_ignore_COMMENT   = r'//.*'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_KEYWORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_QCHAR(t):
    r'\'[a-zA-Z]\''
    t.value = list(t.value)[1]
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def lex(input):
    lexer.input(input)
    return iter(lexer)




##p = '''
##x = 33 + 44;
##return y = x > 66;
##else 'r'
##'''
##
##lexer.input(p)
##while True:
##    tok = lexer.token()
##    if not tok: break
##    print tok
