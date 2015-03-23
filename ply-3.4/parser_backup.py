import ply.yacc as yacc

import lexer # Import lexer information

tokens = lexer.tokens # Need token list


# one or more occurances
def p_program(p):
    '''program : program declaration
               | declaration
    '''

def p_declaration(p):
    '''declaration : fun_declaration
                   | var_declaration
    '''

# Editted to support zero-many formal parameters
def p_fun_declaration(p):
    '''fun_declaration : type NAME LPAR formal_pars RPAR block
                       | type NAME LPAR RPAR block
    '''

# Editted
def p_formal_pars(p):
    '''formal_pars : formal_pars COMMA formal_par
                   | formal_par
    '''

def p_formal_par(p):
    ''' formal_par : type NAME '''

# Editted to support zero-many var declarations, and statements
def p_block(p):
    '''block : LBRACE var_declarations statements RBRACE
             | LBRACE var_declarations RBRACE
    '''

# Editted
def p_var_declarations(p):
    '''var_declarations : var_declaration var_declarations
                        | empty
    '''
    
def p_var_declaration(p):
    '''var_declaration : type NAME SEMICOLON '''
    p[0] = [p[1], p[2] ]
    

def p_type(p):
    ''' type : INT
             | CHAR
             | type LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]

# Editted to support zero-many ;statements
def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statement
    '''

# Editted to support zero pars
def p_statement(p):
    '''statement : IF LPAR exp RPAR statement
		 | IF LPAR exp RPAR statement ELSE statement
		 | WHILE LPAR exp RPAR statement
		 | lexp ASSIGN exp
		 | RETURN exp 
		 | NAME LPAR pars RPAR
		 | NAME LPAR RPAR		
		 | block
		 | WRITE exp
		 | READ lexp
    '''

def p_lexp(p):
    '''lexp : var
            | lexp LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]

#Editted to support empty pars
def p_exp(p):
    '''exp : lexp
           | exp binop exp		
	   | unop exp
	   | LPAR exp RPAR
	   | NUMBER 
	   | NAME LPAR pars RPAR
	   | NAME LPAR RPAR
	   | QCHAR
	   | LENGTH lexp
    '''

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

def p_unop(p):
    '''unop : MINUS
            | NOT
    '''

# Editted to support zero-many parse
def p_pars(p):
    '''pars : pars COMMA exp
            | exp
    '''

def p_var(p):
    '''var : NAME '''
    p[0] = p[1]
    
def p_empty(p):
    '''empty : '''
    pass

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
print "Program 2: ", yacc.parse(p2)
print "Program 3: ", yacc.parse(p3)


