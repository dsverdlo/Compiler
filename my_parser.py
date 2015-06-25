#-------------------------------------------------------------------------------
# Name:         my_parser.py
# Purpose:      Use PLY to define the parsing rules for valid (extended) TINY
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------

import yacc as yacc

import my_lexer as lexer # Import lexer information
import node as node
import backend as backend # can be removed later
from labelmaker import *
from my_assembler import *

tokens = lexer.tokens # Need token list


# Parsing rules

precedence = [
    ('nonassoc'    , 'IF'),
	('nonassoc'    , 'ELSE'),
	('left'        , 'LBRACK', 'RBRACK'),
    ('left'        , 'AND', 'OR'),
	('nonassoc'    , 'NOT'),
	('nonassoc'    , 'EQUAL', 'NEQUAL'),
	('nonassoc'    , 'LESS', 'GREATER'),
	('left'        , 'PLUS', 'MINUS'),
	('left'        , 'TIMES', 'DIVIDE'),
	('nonassoc'    , 'LENGTH'),
	('nonassoc'    , 'RETURN'),
]


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
    '''fun_declaration : fun_type NAME LPAR formal_pars RPAR block SEMICOLON
                       | fun_type NAME LPAR RPAR block SEMICOLON
    '''
    if len(p) == 7:
        p[0] = node.Node('fDecl')
        p[0].add_child(p[1]) # type
        p[0].add_child(p[2]) # name
        p[0].add_child(node.Node('fparams'))
        p[0].add_child(p[5]) # block
    else:
        p[0] = node.Node('fDecl')
        p[0].add_child(p[1]) # type
        p[0].add_child(p[2]) # name
        p[0].add_child(p[4]) # fpars
        p[0].add_child(p[6]) # block


def p_fun_type(p):
    '''fun_type : VOID
               | INT
             | CHAR
             | BOOLEAN
    '''
    p[0] = p[1]


def p_type(p):
    ''' type : INT
             | CHAR
             | BOOLEAN
             | type LBRACK exp RBRACK
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = node.Node('ARRAY')
        p[0].add_child(p[1])
        p[0].add_child(p[3])



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
        p[0].add_child(node.Node('statements'))
    elif len(p) == 5: # both present
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
        p[0] = p[2]
    else:
        p[0] = node.Node('varDecls')

def p_var_declaration(p):
    '''var_declaration : type NAME SEMICOLON '''
    p[0] = node.Node('varDecl')

    if type(p[1]) is node.Node: # array declaration
        p[0].add_child(p[1].children[0]) # type
        p[0].add_child(p[2]) # name
        p[0].add_child(p[1].children[1]) # size
    else:
        p[0].add_child(p[1])
        p[0].add_child(p[2])




# Editted to support zero-many ;statements
def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statement
    '''
    if len(p) == 2:
        p[0] = node.Node('statements')
        p[0].add_child(p[1])
    else:
        p[1].add_child(p[3])
        p[0] = p[1]



# Editted to support zero pars
def p_statement(p):
    '''statement : block
		 | RETURN exp
		 | WRITE exp
		 | READ lexp
		 | NAME LPAR RPAR
		 | NAME LPAR pars RPAR
		 | WHILE LPAR exp RPAR statement
		 | IF    LPAR exp RPAR statement
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
    elif len(p) == 5: # function call
        p[0] = node.Node('fCall')
        p[0].add_child(p[1])
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
        p[0] = node.Node(p[1])
        p[0].add_child(p[2])
    elif len(p) == 4:
        p[0] = p[2]

def p_and(p):
    '''exp : exp AND exp'''
    p[0] = node.Node('and')
    p[0].add_child(p[1])
    p[0].add_child(p[3])

def p_or(p):
    '''exp : exp OR exp'''
    p[0] = node.Node('or')
    p[0].add_child(p[1])
    p[0].add_child(p[3])


def p_fun_call(p):
    '''exp : NAME LPAR RPAR
	   | NAME LPAR pars RPAR
    '''
    p[0] = node.Node('fCall')
    p[0].add_child(p[1])
    if len(p) == 5: # if there are pars: add them
        for c in p[3].children:
            p[0].add_child(c)


def p_number(p):
    '''exp : NUMBER '''
    p[0] = node.Node('NUMBER')
    p[0].add_child(p[1])

def p_qchar(p):
    '''exp : QCHAR '''
    p[0] = node.Node('QCHAR')
    p[0].add_child(p[1])

def p_binop_exp(p):
    ''' exp : exp MINUS exp
            | exp PLUS exp
            | exp TIMES exp
            | exp DIVIDE exp
            | exp EQUAL exp
            | exp NEQUAL exp
            | exp GREATER exp
            | exp LESS exp
            | exp GREATEREQ exp
            | exp LESSEQ exp
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
    p[0] = node.Node('VAR')
    p[0].add_child(p[1])


def p_bool(p):
    '''exp  : TRUE
            | FALSE'''
    p[0] = node.Node('BOOL')
    p[0].add_child(p[1])


def p_empty(p):
    '''empty : '''
    pass # edit
    #p[0]= node.Node()

# Error rule for syntax errors
def p_error(p):
    print 'Syntax error: ', p





parser = yacc.yacc() # Build the parser


def parse(code):
    return parser.parse(code)

