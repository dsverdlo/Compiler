import yacc as yacc

import lexer # Import lexer information

tokens = lexer.tokens # Need token list


# one or more occurances
def p_program(p):
    '''program : declaration program
               | declaration
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_declaration(p):
    '''declaration : fun_declaration
                   | var_declaration
    '''
    p[0] = p[1]

# Editted to support zero-many formal parameters
def p_fun_declaration(p):
    '''fun_declaration : type NAME LPAR formal_pars RPAR block
                       | type NAME LPAR RPAR block
    '''
    if len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    else:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

# Editted
def p_formal_pars(p):
    '''formal_pars : formal_pars COMMA formal_par
                   | formal_par
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

def p_formal_par(p):
    ''' formal_par : type NAME '''
    p[0] = (p[1], p[2])

# Editted to support zero-many var declarations, and statements
def p_block(p):
    '''block : LBRACE var_declarations statements RBRACE
             | LBRACE var_declarations RBRACE
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3], p[4])

# Editted
def p_var_declarations(p):
    '''var_declarations : var_declaration var_declarations
                        | empty
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
    
def p_var_declaration(p):
    '''var_declaration : type NAME SEMICOLON '''
    p[0] = (p[1], ('NAME',p[2]))
    

def p_type(p):
    ''' type : INT
             | CHAR
             | type LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3], p[4])

# Editted to support zero-many ;statements
def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statement
    '''
    if len(p) == 2:
        p[0] = (p[1])
    else:
        p[0] = (p[1] + (p[2], p[3]))

# Editted to support zero pars
def p_statement(p):
    '''statement : block		
		 | RETURN exp 
		 | WRITE exp
		 | READ lexp
		 | NAME LPAR RPAR
		 | NAME LPAR pars RPAR
		 | WHILE LPAR exp RPAR statement
		 | IF LPAR exp RPAR statement
		 | IF LPAR exp RPAR statement ELSE statement
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3],p[4])
    elif len(p) == 6:
        p[0] = (p[1], p[2], p[3],p[4],p[5])
    elif len(p) == 7:
        p[0] = (p[1], p[2], p[3],p[4],p[5],p[6])
    elif len(p) == 8:
        p[0] = (p[1], p[2], p[3],p[4],p[5],p[6],p[7])

def p_assign(p):
    '''statement : lexp ASSIGN exp'''
    p[0] = (p[2], p[1], p[3])
    
def p_lexp(p):
    '''lexp : var
            | lexp LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3], p[4])

#Editted to support empty pars
def p_exp(p):
    '''exp : lexp	
	   | LENGTH lexp	
	   | unop exp
	   | LPAR exp RPAR
	   | NAME LPAR RPAR
	   | NAME LPAR pars RPAR
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p)== 3:
        p[0] = (p[1], p[2])
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])

def p_number(p):
    '''exp : NUMBER '''
    p[0] = ('NUMBER', p[1])

def p_qchar(p):
    '''exp : QCHAR '''
    p[0] = ('QCHAR', p[1])
    
def p_unop_exp(p):
    ''' exp : exp binop exp '''
    p[0] = (p[2], p[1], p[3])

def p_binop(p):
    '''binop : MINUS
	     | PLUS
	     | TIMES
	     | DIVIDE
	     | EQUAL
	     | NEQUAL
	     | GREATER
	     | LESS
    '''
    p[0] = p[1]

def p_unop(p):
    '''unop : MINUS
            | NOT
    '''
    p[0] = p[1]

# Editted to support zero-many parse
def p_pars(p):
    '''pars : pars COMMA exp
            | exp
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

def p_var(p):
    '''var : NAME '''
    p[0] = ('NAME', p[1])
    
def p_empty(p):
    '''empty : '''
    #pass
    p[0]= ()

# Error rule for syntax errors
def p_error(p):
    print 'Syntax error: ', p
 
yacc.yacc() # Build the parser

# Parsing rules

precedence = [
        ('nonassoc', 'IF'),
	('nonassoc', 'ELSE'),
	('left',     'LBRACK', 'RBRACK'),
	('nonassoc', 'NOT'),
	('nonassoc', 'EQUAL', 'NEQUAL'),
	('nonassoc', 'LESS', 'GREATER'),
	('left',     'PLUS', 'MINUS'),
	('left',     'TIMES', 'DIVIDE'),
	('nonassoc', 'LENGTH'),
	('nonassoc', 'RETURN'),

]






p1 = '''
int f(int[1] a) {
    char c;
    int a1; // comment
    int[12] a2;
    c = 10;
    a2[9] = 12;
    return a2[9] > 5
}
'''

p2 = '''
int f(int[1] a, char b, int c) {
    char d;
    d = 'r'
}
'''

p3 = '''
char fun(int fp1, int fp2) {
    return doSomething[5]
} '''

print "Program 1: ", yacc.parse(p1)
#print "Program 2: ", yacc.parse(p2)
#print "Program 3: ", yacc.parse(p3)

yacc.parse('''
char fname(int x) {
    x = 5 - 1; // noob
    return x
}
''')
