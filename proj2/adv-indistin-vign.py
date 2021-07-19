#
# Adversarial Indistinguishability Experiment
# CSC507/609 Term 201
#
# Write an adversary with an advantage in the
# indistinguishability game for a vigenere cipher.
# The key is generated according to the distribution
# presented in problem 2.8 of the class text.
#
# template author: bjr
# template date: 9 sept 2019


# please enter name and date: Kerui Zeng 16 spet 2019
# student name: Kerui Zeng
# date (last update): 17 Sept 2019
import string
import os
import numpy as np
import argparse
import sys
import random

### Encipherment and key generator functions

def vigenere_encipher(p,k):
	"""
	p is plaintext over the alphabet a, b, c, ... , z
	c is ciphertext over the alphabet A, B, C, ... , Z
	k is a string over the alphabet, the keyword, e.g. "keyword"
	"""
	if args_g.verbose:
		print("cycle_enigma_encipher:")
		print("\tplaintext:",p)
		print("\tkey:",k)


	c = ""
	kord = [ ord(kc)-ord('a') for kc in k ]
	i = 0
	for pi in p:
		#
# replace next line
		x = ord(pi)-ord('a')
		j = kord[i] 
		y = (x+j) % 26
		c += chr(y+ord('A'))
		i += 1
		if i >= len(kord):
			i = 0
		#
	return c 

def gen_key(n):
	key_size = random.choice(range(n))
	#key_size = n
	i = 0 
	k=''
	for i in range(key_size):
		num = random.choice(range(26))
		one_key = chr( num + ord('a') )
		k = k + one_key
	#print(k)
	return k


### Adversary functions

def gen_bit():
	return random.choice([0,1])


def adversary_challenge():
	# adversary chooses a message pair
	#
# replace next line
	f0 = open('gettysburg.txt')
	m0 = f0.read()
	f0.close()
# replace next line
	f1 = open('m1.txt')
	m1 = f1.read()
	f1.close()
	#
	return (m0,m1)


def adversary_decision(m0,m1,c):
	# adversary takes the encryption c of
	# either m0 or m1 and returns a best
	# guess of which message was encrypted
	#
	# This code is highly dependent on the
	# cipher used. It is the heart of the crack.
	#
# replace next line
	p =""
	ioc = cal_ioc(c,len(c)*3/4)
	key_length_guess = count_intervals_of_ioc(ioc)
	key_length = key_length_guess

	fc = get_statistics()
	if args_g.verbose:
		print (fc)
	
	list_split = split_into_length_part(key_length, c)
	list_split_count = fc_for_sublist(list_split)
	key_in_number = collect_all_key(list_split_count,fc)
	key_in_letter = number_to_letter(key_in_number)
	key = "".join(key_in_letter)
	p = vigenere_decipher(c,key)
	
	prob_m0 = 0.0
	prob_m1 = 0.0
	same_num_m0 = 0.0
	same_num_m1 = 0.0
	all_num = len(p)
	
	for i in range(len(p)):
		if p[i] == m0[i]:
			same_num_m0 +=1
	prob_m0 = same_num_m0 / all_num
	
	for i in range(len(p)):
		if p[i] == m1[i]:
			same_num_m1 +=1
	prob_m1 = same_num_m1 / all_num
	if prob_m0 > prob_m1:
		guess = 0
	else:
		guess = 1
	#
	return guess


def adversary_start():
	# adversary chooses a message pair
	return adversary_challenge()


def adversary_sample(m):
	# the adversarial indistinguishability experiment
	# a bit is chosen at random
# replace next line
	b = gen_bit()
	#
	# a cipher key is chosen at random
# replace next line
	k ='' 
	while len(k) <= 0:
		k = gen_key(len(m[b]))

	#
	# the cipher is queried with key k and message m[b]
# replace next line
	c = vigenere_encipher(m[b],k)
	#
	# the adversary makes its guess
# replace next line
	guess = adversary_decision(m[0],m[1],c)
	#
	return b==guess


def adversary_advantage(trials):

	if args_g.verbose:
		print("number trials:", trials)

	m = adversary_start()
	count = 0 
	for i in range(trials):
		if adversary_sample(m):
			count += 1
	return (count+0.0)/(trials+0.0)


def encodearray(p):
	
	l = []
	for c in p:
		l.append(ord(c.lower())-ord('a'))
	return np.array(l)

def cal_ioc (p,n):
	n = int(n)	
	ca = encodearray(p)
	ioc = []
	for i in range(n):
		ioc.append(np.sum(ca == np.roll(ca,i)))
	ioc[0] = 0
	return ioc

def count_intervals_of_ioc(ioc):
	
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


def frequencycount(s):
	count = [0] * 26
	for c in s :
		i = ord(c.lower())-ord('a')
		count[i] += 1
	return count

def get_statistics():
	f = open("m1.txt","r")
	p = "" 
	for line in f:
		for c in line :
			if c.isalpha() :
				p = p + c.lower() 
	f.close() 
	return frequencycount(p)

def split_into_length_part(key_length, t_in):
	list_of_t = list(t_in)
	list_spilt = []
	for i in range(key_length):
		sublist = list_of_t[i :: key_length]
		list_spilt.append(sublist)
	return list_spilt


def fc_for_sublist(list_split):
	list_split_count = []
	for i in range(len(list_split)):
		sublist_count = frequencycount(list_split[i])
		list_split_count.append(sublist_count)
	#print(list_split_count)
	return list_split_count

def guess_sublist_key(sublist_count, fc):
	max = 0
	value = 0
	key = 0
	for i in range(len(sublist_count)):
		roll_list = np.roll(sublist_count, 0 - i)
		value = sum_of_two_list(roll_list,fc)
		if value > max:
			max = value
			key = i
		value = 0
		return key   
 
def sum_of_two_list(roll_list,fc):
	value = 0
	for i in range(len(roll_list)):
		value = value + roll_list[i] * fc[i]
	return value

def collect_all_key(list_split_count,fc):
	final_key = []
	for i in range(len(list_split_count)):
		key = guess_sublist_key(list_split_count[i],fc)
		final_key.append(key)
	#print(final_key)
	return final_key

def number_to_letter(key_in_number):
	key_in_letter = []
	for i in key_in_number:
		letter = chr(i+ord('a'))
		key_in_letter.append(letter)
	return key_in_letter

def vigenere_decipher(c,k):
	p = ""
	#
	# code
	#
	i = 0
	for ci in c:
		y = ord(ci) - ord('A')
		j = ord(k[i].lower()) - ord('a')
		x = (y-j)% 26
		p = chr(x+ord('a'))
		i += 1
		if i >= len(k):
			i = 0
	return p 


# main

def parse_args():
	parser = argparse.ArgumentParser(description="The adversary protocol game for a vigenre cipher.")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	parser.add_argument("-k", "--keyword", help="set keyword and trigger encryption mode")
	parser.add_argument("argument", help="depening on mode, either number of trials or the plaintext to encrypt ")
	
	return parser.parse_args()

def main(argv):
	global args_g
	args_g = parse_args()

	if args_g.keyword == None:
		print (adversary_advantage(int(args_g.argument)))
	else:
		print (vigenere_encipher(args_g.argument, args_g.keyword))


if __name__ == "__main__":
	main(sys.argv)




