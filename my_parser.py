import yacc as yacc

import my_lexer as lexer # Import lexer information
import node as node
import backend as backend # can be removed later
from labelmaker import *
from my_assembler import *

tokens = lexer.tokens # Need token list


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


# TAC = tac.Tac()

# one or more occurances
def p_program(p):
    '''program : declaration program
               | declaration
    '''
    if len(p) == 2:
        if not type(p[0]) is node.Node:
            p[0] = node.Node('program')
        p[0].add_child(p[1])
    else:
        p[2].ins_child(p[1])
        p[0] = p[2]

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
        #p[0] = ('FUN', (p[1], p[2]), p[3], p[4], p[5])
        p[0] = node.Node('FUNCTION')
        p[0].add_child(p[1]) # type
        p[0].add_child(p[2]) # name
        p[0].add_child(node.Node('fparams')) # todo work out
        p[0].add_child(p[5]) # block
    else:
        p[0] = node.Node('FUNCTION')
        p[0].add_child(p[1]) # type
        p[0].add_child(p[2]) # name
        p[0].add_child(p[4]) # fpars
        p[0].add_child(p[6]) # block

# Editted
def p_formal_pars(p):
    '''formal_pars : formal_pars COMMA formal_par
                   | formal_par
    '''
    if len(p) == 2:
        p[0] = node.Node('fparams')
        p[0].add_child(p[1])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]

def p_formal_par(p):
    ''' formal_par : type NAME '''
    p[0] = node.Node('fparam')
    p[0].add_child(p[1])
    p[0].add_child(p[2])


# Editted to support zero-many var declarations, and statements
def p_block(p):
    '''block : LBRACE var_declarations statements RBRACE
             | LBRACE var_declarations RBRACE
    '''
    if len(p) == 4:
        p[0] = node.Node('block')
        p[0].add_child(p[2])
    elif len(p) == 5:
        p[0] = node.Node('block')
        p[0].add_child(p[2])
        p[0].add_child(p[3])

# Editted
def p_var_declarations(p):
    '''var_declarations : var_declaration var_declarations
                        | empty
    '''
    if len(p) == 3:
        p[2].ins_child(p[1])
        #p[0].add_child(p[2])
        p[0] = p[2]
    else:
        p[0] = node.Node('variables') #p[1]

def p_var_declaration(p):
    '''var_declaration : type NAME SEMICOLON '''
    p[0] = node.Node('var')
    p[0].add_child(p[1])
    p[0].add_child(p[2])


def p_type(p):
    ''' type : INT
             | CHAR
             | type LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = node.Node('array_index')
        p[0].add_child(p[1])
        p[0].add_child(p[3])

# Editted to support zero-many ;statements
def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statement
    '''
    if len(p) == 2:
        p[0] = node.Node('STATEMENTS')
        p[0].add_child(p[1])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]
##    ''' statements : statements statement
##                   | statement SEMICOLON
##    '''
##    if p[2] == ';':
##        p[0] = node.Node('STATEMENTS')
##        p[0].add_child(p[1])
##    else:
##        p[1].add_child(p[2])
##        p[0] = p[1]


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
    elif len(p) == 3: # return write read
        p[0] = node.Node(p[1])
        p[0].add_child(p[2])
    elif len(p) == 4: # function call with no pars
        p[0] = node.Node('fCall')
        p[0].add_child(p[1])
        p[0].add_child(node.Node()) # empty
    elif len(p) == 5: # function call
        p[0] = node.Node('fCall')
        p[0].add_child(p[1])
        #p[0].add_child(p[3])
        for c in p[3].children:
            p[0].add_child(c)
    elif len(p) == 6: # while or if
        p[0] = node.Node(p[1])
        p[0].add_child(p[3])
        p[0].add_child(p[5])
    elif len(p) == 8: # if then else
        p[0] = node.Node(p[1])
        p[0].add_child(p[3])
        p[0].add_child(p[5])
        p[0].add_child(p[7])

def p_assign(p):
    '''statement : lexp ASSIGN exp'''
    #p[0] = (p[2], p[1], p[3])
    #print(TAC.genCopy(p[1], p[3]))
    p[0] = node.Node('assign')
    p[0].add_child(p[1])
    p[0].add_child(p[3])

def p_lexp(p):
    '''lexp : var
            | lexp LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = node.Node('array_access')
        p[0].add_child(p[1])
        p[0].add_child(p[3])

#Editted to support empty pars
def p_exp(p):
    '''exp : lexp
	   | LENGTH lexp
	   | unop exp
	   | LPAR exp RPAR
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p)== 3: # length or unary
        p[0] = node.Node(p[1])#tokens.index(p[1]))
        p[0].add_child(p[2])
    elif len(p) == 4:
        p[0] = p[2]

def p_fun_call(p):
    '''exp : NAME LPAR RPAR
	   | NAME LPAR pars RPAR
    '''
    p[0] = node.Node('fCall')
    #print "I see a " + str(p[1])
    p[0].add_child(p[1])
    if len(p) == 5: # if there are pars: add them
        #p[0].add_child(p[3])
        for c in p[3].children:
            #print "Adding it, chillout ***"
            p[0].add_child(c)
    else:
        pass#p[0].add_child(node.Node()) # otherwise empty node


def p_number(p):
    '''exp : NUMBER '''
    #p[0] = node.Node('NUMBER')
    #p[0].add_child(p[1])
    p[0] = p[1]

def p_qchar(p):
    '''exp : QCHAR '''
    #p[0] = node.Node('QCHAR')
    #p[0].add_child(p[1])
    p[0] = p[1]

def p_binop_exp(p):
    #''' exp : exp binop exp '''
    ''' exp : exp MINUS exp
            | exp PLUS exp
            | exp TIMES exp
            | exp DIVIDE exp
            | exp EQUAL exp
            | exp NEQUAL exp
            | exp GREATER exp
            | exp LESS exp
    '''
    p[0] = node.Node(p[2])
    p[0].add_child(p[1])
    p[0].add_child(p[3])


def p_unop(p):
    '''unop : MINUS
            | NOT
    '''
    p[0] = p[1]

# Editted to support zero-many pars
def p_pars(p):
    '''pars : pars COMMA exp
            | exp
    '''
    if len(p) == 2:
        p[0] = node.Node('params')
        p[0].add_child(p[1])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]

def p_var(p):
    '''var : NAME '''
    #p[0] = node.Node('NAME')
    #p[0].add_child(p[1])
    p[0] = p[1]

def p_empty(p):
    '''empty : '''
    #pass
    p[0]= node.Node()

# Error rule for syntax errors
def p_error(p):
    print 'Syntax error: ', p





parser = yacc.yacc() # Build the parser


def parse(code):
    return parser.parse(code)

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
int big;
int f(int[1] a, char b, int c) {
    char d;
    int a;
    char b;

    d = 'r';
    b = d + 1;

    return f(a, b, d);

    unreachable = 4 + 5
}
int g() {
   int second;
   second = 2;
   return second;
   b = 5 - useless;
   return again
}
'''

p3 = '''
char fun(int fp1) {
    int counter;
    counter = 1;
    if(fp1 > counter) {
        squareCounter(xxx, yyyy);
        fp1 = fp - 1
    };
    return counter

} '''

p4 = '''
int a;
int fun() {
    a[5] = b * c + b * c

} '''

p5 = '''
int foo() {
    int x;
    int y;
    x = 14;
    y = 8 - x / 2;
    x = 2;
    return y * (28 / x + 2);
    x = 5

}
'''
p6 = '''
int foo() {
    z = 5 > 6
}'''
p7 = '''
int foo() {
    while(a<b) {
        if(c<d) {
           x = y + z
        }
    }
}'''
p8 = '''
int ifff() {
    if(cond1) {
        return a
    };
    if(1 > 2) {
        return 1
    } else {
        return 2
    };
    while(x > 0) {
        x = x - 1
    }
}
'''

foldconst = '''
int f(int j) {
  int i;
  i= 3;
  if (j > 0)
    i = 4
  else
    j = 1;
  return i
}

int g(int j) {
  int i;
  i = 3;
  if (j > 0)
    j = j+1
  else
    j = -j;
  return i
}

int
main() {
 write f(2);
 write g(3)
}
'''

ifeq = '''
int main() {
  int x;
  int y;
  x = (1 + 2) / 3;
  write x;
  return x;
  write y
}
'''
#print "Program 1: ", parser.parse(p1)
#print "Program 2: ", parser.parse(p2)
#print "Program 3: ", parser.parse(p3)

#print "Program 4: ", parser.parse(p5).toString()
#print "Optimise AST: ", backend.optimise(parser.parse(p5))
#pp3 = parser.parse(p3)
#backend.flatten_instructions(pp3, labelmaker())
#backend.assemble(pp3)

#addition = parser.parse(p6).children[0].children[3].children[1].children[0].children[1]
#backend.assemble(addition)

#fcall = parser.parse(p7).children[0].children[3].children[1].children[0]
#backend.assemble(fcall)

#iff = parser.parse(p8)
#backend.assemble(iff)
#backend.assemble(iff.children[0].children[2].children[1].children[0])
#backend.assemble(iff.children[0].children[2].children[1].children[1])

#fc = parser.parse(foldconst)
#backend.assemble(fc)


#ife = parser.parse(ifeq)

#print " *** 1 Substituting nested instructions *** "
#backend.flatten_instructions(ife, labelmaker())

#print " *** 2 Optimising *** "
#backend.optimise(ife)

#print " *** 3 Printing results *** "
#print ife
#a = assembler()
#a.assemble(ife)
#a.write_to_file('test.asm')


#ifebody = ife.children[0].children[3].children[1]
#fcc = backend.flatten_instructions(ifebody, l)

##fcc
##print(parser.parse('''
##char fname(int x, int y, int z) {
##    x = 5 - 1; // noob
##    return x
##}
##''')
##)

