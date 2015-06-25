@echo off

copy output.asm "C:\Program Files (x86)\CodeBlocks\MinGW\bin"

cd "C:\Program Files (x86)\CodeBlocks\MinGW\bin"

nasm.exe -f win32 output.asm

echo NASMED 

gcc output.obj driver.c asm_io.obj 

echo GCCED 

a.exe

cd "C:\Users\david\Documents\Studies\VUB\2014-2015\Compilers(6stp)\Project\Compiler"