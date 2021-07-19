#
# makefile for csc507/609 semester 201
# author: bjr
# date: 24 sep 2019
#

LIB= PYTHONPATH="../../class/modules"
PY3= python3
#VERBOSE= -v
VERBOSE=

F1= blowfish_test.py
F2= rijndael_test.py
F3= encrypt.py

PWD= "the key phrase" 

G= gettysburg.txt

all:
	make run

run:
	echo "hello world" | ${LIB} ${PY3} ${F3} ${VERBOSE} -m cbc -p pkcs ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m cbc -p pkcs ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	echo "hello world" | ${LIB} ${PY3} ${F3} ${VERBOSE} -m ofb -p iso ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m ofb -p iso ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	echo "hello world" | ${LIB} ${PY3} ${F3} ${VERBOSE} -m cntr -p pkcs ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m cntr -p pkcs ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	make clean

run2:
	cat $G | ${LIB} ${PY3} ${F3} ${VERBOSE} -m cbc -p pkcs ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m cbc -p pkcs ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	cmp decrypt.out $G
	cat $G  | ${LIB} ${PY3} ${F3} ${VERBOSE} -m ofb -p iso ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m ofb -p iso ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	cmp decrypt.out $G
	cat $G | ${LIB} ${PY3} ${F3} ${VERBOSE} -m cntr -p pkcs ${PWD} > encrypt.out
	cat encrypt.out | ${LIB} ${PY3} ${F3} ${VERBOSE} -d -m cntr -p pkcs ${PWD} > decrypt.out
	cat encrypt.out | hexdump -C
	cat decrypt.out | hexdump -C
	cmp decrypt.out $G
	make clean




	
help-message:
	${LIB} ${PY3} ${F3} -h

libtest:
	${LIB} ${PY3} ${F1}
	${LIB} ${PY3} ${F2}

clean:
	-rm encrypt.out
