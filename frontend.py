#-------------------------------------------------------------------------------
# Name:         frontend.py
# Purpose:      Read commandline arguments and display compiling information
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------
import sys, os
import my_parser as prsr
from backend import optimise, flatten_instructions
from my_assembler import assembler
from typechecker import type_check
from labelmaker import labelmaker

def main():

    # Create a file with the Intermediate Representation
    def write_ir(ast, fileout):
        filename = os.path.splitext(fileout)[0]
        with open(filename + ".ast", 'w') as file:
            file.write(ast.toFileString())


    def execute(code, fileinname, fileoutname):
        typecheckerrors = []

        print "\n***** 1 Parsing the program *** "
        result = prsr.parse(code)

        if result is None:
            print "\n !!! Errors found in program !!!"
            return
        #debug
        print result.toString()

        print "\n***** 2 Substituting nested instructions *** "
        flatten_instructions(result, labelmaker(), typecheckerrors)
        if typecheckerrors != []:
            print "\n !!! Type check errors found !!!"
            for error in typecheckerrors:
                print "\n !!! --> {}".format(error)
            return

        print "\n***** 2.5 Performing type check *** "
        type_check(result, typecheckerrors)

        if typecheckerrors != []:
            print "\n !!! Type check errors found !!!"
            for error in typecheckerrors:
                print "\n{}".format(error)
            return

        print "\n***** 3 Applying optimisations *** "
        optimise(result)

        # Write intermediate code representation
        write_ir(result, fileoutname)

        print "\n***** 4 Assembling AST *** "
        asm = assembler(result)

        print "\n***** 5 Writing file out: " + fileoutname
        asm.write_to_file(fileinname, fileoutname)

        print "\n***** PROCESS TERMINATED *** "

    # file out name is calculated, now  see if a file or raw code is given
    def process_file_or_code(given, fileoutname):
        if os.path.exists(given):
            extension = os.path.splitext(given)[1]
            if extension.lower() != '.tiny':
                print "\nError: Expected a file with the TINY extension."
                print "\nUsage: frontend.py fileinname [fileoutname]"
                print "   or  frontend.py sourcecode [fileoutname]"
                return 2

            print "\n *** Received file: {} *** ".format(given)
            code = ""
            with open(given, 'r') as f:  # this closes the file after reading
                code = f.read()
            execute(code, given, fileoutname)

        else:
            print "\n *** Received raw code. This better be tiny code... *** "
            execute(given, '<RAW CODE>', fileoutname)


    if len(sys.argv) < 2:
        print "\nError: Expected a filename or path+filename to a .tiny file or a TINY program code"
        print "\nUsage: frontend.py [options] fileinname [fileoutname]"
        print "   or  frontend.py [options] sourcecode [fileoutname]"
        print "\nWhere [options] are:"
        print "   -v   Display verbose output"
        return 1

    if len(sys.argv) < 3:  # 1 arg --> fileoutname = fileinname
        if os.path.exists(sys.argv[1]):
            pathfilename = os.path.splitext(sys.argv[1])[0] # split path+fname and ext
            filename = os.path.split(pathfilename)[1]
            process_file_or_code(sys.argv[1], "{}{}{}.asm".format(os.getcwd(),os.path.altsep,filename))
        else:
            process_file_or_code(sys.argv[1], "{}{}output.asm".format(os.getcwd(),os.path.altsep))

    elif len(sys.argv) == 3:  # 2 args --> [1] file/code, [2] fileoutname
        if os.path.splitext(sys.argv[2])[1] == '':
            sys.argv[2] += '.asm'

        process_file_or_code(sys.argv[1], "{}{}{}".format(os.getcwd(),os.path.altsep,sys.argv[2]))



if __name__ == '__main__':
    main()
