import string
import sys
import os
import argparse
import numpy as np
#
# crack-vigenere.py
#
# author:
# date: 
# last update:
# template by: bjr aug 2019
#

args_g = 0  # args are global

def frequencycount(s):
	count = [0] * 26
	for c in s :
		i = ord(c.lower())-ord('a')
		count[i] += 1
	return count

def get_statistics(filename):
	f = open(filename,"r")
	p = "" ;
	for line in f:
		for c in line :
			if c.isalpha() :
				p = p + c.lower() ;
	f.close() ;
	return frequencycount(p) ;


	#
	# code
	#
#key_length = args_g.key_length
	
def split_into_length_part(key_length, t_in):
	list_of_t = list(t_in)
	list_spilt = []
	for i in range(key_lengh):
		sublist = list_of_t[i :: key_length]
		list_spilt.append(sublist)
	return list_spilt

def fc_for_sublist(list_split):
	list_split_count = []
	for i in range(len(list_split)):
			for j in list_split[i]:
				sublist_count = frequencycount(list_split[i])
				list_spilt_count.append(sublist_count)
	return list_spilt_count

def guess_sublist_key(sublist_count, fc):
	max = 0;
	value = 0;
	key = 0;
	for i in range(len(sublist_count)):
		np.roll(sublist_count,i)
		for j in range(len(sublist_count)):
			value =+ fc[i] * sublist_count[i] 
		if value > max:
			key = i
	return key;    

def collect_all_key(list_split_count,fc):
	final_key = []
	for i in range(len(list_split_count)):
		key = guess_sublist_key(list_split_count[i],fc)
		final_key.append(key)
	return final_key

def number_to_letter(key_in_number):
	key_in_letter = []
	for i in range(len(key_in_number)):
		letter = chr(ord(i)+ord('a'))
		key_in_letter.append(letter)
	return key_in_letter

def parse_args():
	parser = argparse.ArgumentParser(description="Cracks a vigenere cipher by freqency analysis, given the key length.")
	parser.add_argument("key_length", type=int, help="the presumed length of the encipherment key")
	parser.add_argument("reference_text", help="a text file sampling the letter frequence statistics")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	return parser.parse_args()

def main(argv):

	global args_g
	args_g = parse_args()

	fc = get_statistics(args_g.reference_text)
	if args_g.verbose:
		print (fc)

	## gather plain text and format
	t_in = ""
	for line in sys.stdin:
		for c in line:
			if c.isalpha():
				t_in += c

	if args_g.verbose:
		print (t_in)

	#
	# code
	#
	key_length = args_g.key_length
	list_split = split_into_length_part(key_length, t_in)
	list_split_count = fc_for_sublist(list_split)
	key_in_number = collect_all_key(list_split_count,fc)
	key_in_letter = number_to_letter(key_in_number)
	password = "".join(key_in_letter)
	print (password)


main(sys.argv)
