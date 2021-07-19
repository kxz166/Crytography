#
# makefile for proj1
# author: bjr
# date: 2 feb 2018
#

I= gettysburg.txt
KEY= abc
#VERBOSE= -v
#MF= -f Makefile-class

all:
	make ${MF} test-vigenere
	make ${MF} test-ioc
	make ${MF} test-crack

test-vigenere:
	cat $I | python vigenere.py ${KEY} > vigenere.out
	-diff -w vigenere.out proj1-ref1.txt
	cat proj1-ref1.txt | python vigenere.py -d ${KEY} > vigenere.out
	-diff -w vigenere.out proj1-ref2.txt
	-rm vigenere.out
	
test-ioc:
	cat proj1-ref1.txt | python ioc.py  ${VERBOSE} > ioc.out
	cat $I | python vigenere.py liberty | python ioc.py ${VERBOSE} >> ioc.out
	cat $I | python vigenere.py jefferson | python ioc.py ${VERBOSE} >> ioc.out
	-diff ioc.out proj1-ref3.txt
	-rm ioc.out

test-crack:
	cat proj1-ref1.txt | python  crack-vigenere.py ${VERBOSE} 3 $I > crack.out
	cat $I | python vigenere.py liberty | python crack-vigenere.py ${VERBOSE} 7 $I >> crack.out
	cat $I | python vigenere.py jefferson | python crack-vigenere.py ${VERBOSE} 7 $I >> crack.out
	-diff crack.out proj1-ref4.txt
	-rm crack.out 
