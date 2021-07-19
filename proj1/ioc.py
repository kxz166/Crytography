import string
import sys
import os
import argparse
import numpy as np
#
# ioc.py
#
# author:
# date: 
# last update:
# template by: bjr aug 2019
#


args_g = 0  # args are global

def parse_args():
	parser = argparse.ArgumentParser(description="Calculate index of coincidence over stdin, writing result to stdout.")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	return parser.parse_args()

def main(argv):

	global args_g
	args_g = parse_args()

	## gather input
	t = ""
	for line in sys.stdin:
		for c in line:
			if c.isalpha():
				t += c

	#
	# code
	# 
	ioc = calcioc(t,len(t)*3/4)
	key_length_guess = count_intervals_of_ioc(ioc)
	print (key_length_guess)
	

def encodearray(p):
	# change cipher_text into number between 0-25
	l = []
	for c in p:
		l.append(ord(c.lower())-ord('a'))
	return np.array(l)

def calcioc (p,n):
	# n is how many times we roll the cipher_text
	# p is the cipher_text
	#ioc is an array that in each time of roll, the number of bits are the same
	ca = encodearray(p)
	ioc = []
	for i in range(n):
		ioc.append(np.sum(ca == np.roll(ca,i)))
	ioc[0] = 0
	return ioc

def count_intervals_of_ioc(ioc):
	# peak_array is an array of ioc indexes,and the indexes are the peaks (greater than mean)
	# in ioc array
	peak_array = []
	first_mid = (np.min(ioc)+np.max(ioc)) / 2
	new_ioc = []
	count_array = []
	for i in range(len(ioc)):
		if ioc[i] > first_mid:
			new_ioc.append(ioc[i])
			
	second_mid = (np.min(new_ioc)+np.max(new_ioc)) / 2
	mid = (first_mid + second_mid)/2
	for i in range(len(ioc)):
		if i != 0 and i < len(ioc) - 1 and ioc[i-1] < ioc[i] and ioc[i] > ioc[i+1] and ioc[i] > mid:
			peak_array.append(i) 	

	for i in range(len(peak_array)):
		if i > 0 :	
			interval = peak_array[i] - peak_array[i-1]
			count_array.append(interval)
	final_interval = np.bincount(count_array)
	result = np.argmax(final_interval)
	return result
	
	
	
		


main(sys.argv)
