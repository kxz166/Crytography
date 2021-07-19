#
# template author: bjr
# template date: 9 sept 2019


# please enter name and date:Kerui Zeng 20 sept 2019
# student name:Kerui Zeng
# date (last update):21 sept 2019

import argparse
import sys
import random

### Encipherment and key generator functions

def cycle_enigma_encipher(p,k):
	"""
	k is a list giving the permutation, e.g. [0,2,1]
	p is plaintext over an alphabet a, b, c, .. up to len(k) characters
	c is ciphertext over same alphabet but capital letters, A, B, C, ...
	
	"""
	if args_g.verbose:
		print("cycle_enigma_encipher:")
		print("\tplaintext:",p)
		print("\tkey:",k)

# code here
	k_list = k
	p_list = encode_alpha_key(p)
	
	valid_p = []
	for each in p_list:
		if each in k_list:
			valid_p.append(each)

	i = 0
	j = 0
	p_letter = -1
	c_in_number = []
	#p_in_number = encode_alpha_key(valid_p)
	lens = len(valid_p)
	for i in range(lens):
		index = valid_p[i]
		j = 0
		while j <= i:
			p_letter = k_list[index]
			index = p_letter
			j += 1
		c_in_number.append(p_letter)
		i += 1
	c = "".join(number_to_letter(c_in_number))
	return c 

def gen_key(n):
#
#	generate a random key and return
#	
	if n >= 26:
		n = 26
	if n <= 0:
		n = 1
	
	ls = []
	i = 0
	m = n-1
	one_key = 0
	while i < m:
		
		if one_key in ls:
			one_key = random.choice(range(m))
			#print(one_key)
		elif one_key not in ls:
			ls.append(one_key)
			i +=1
		#print(ls)
		#print("---------",i)
	#letter_list = number_to_key(ls)
	#key = "".join(letter_list)
	#k_list = encode_alpha_key(k)
	return ls 
	#return [i for i in range(n)]  # a boring non-random key

def encode_alpha_key(k):
	return 	[ ord(kc)-ord('a') for kc in k ]

def number_to_letter(k):
	return 	[ chr(kc + ord('A')) for kc in k ]

def number_to_key(k):
	return 	[ chr(kc + ord('a')) for kc in k ]

def cipher_to_number(k):
	return 	[ ord(kc)-ord('A') for kc in k ]

### Adversary functions

def gen_bit():
	return random.choice([0,1])


def adversary_challenge():
	# adversary chooses a message pair
	#
	# 
	f0 = open('abc.txt')
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

	c_in_num = cipher_to_number(c)
	part1 = len(c_in_num)/26+1
	check_list = [[0 for x in range(26)] for y in range(part1)]
	
	#print(check_list)
	j = 0
	m = 0
	i = 0
	while i <= part1:
		check_list[i][j] = (c_in_num[m])
		j += 1
		m += 1
		if m == (len(c_in_num)-1):
			break
		#print(check_list)
		if j > 25:
			j = 0
			i += 1

	check_number = []
	for each in check_list:
		check_number.append(find_same_number(each))
	
	count = 1
	signal = check_number[0]
	for each in check_number:
		if each == signal:
			count += 1
	
	if count - len(check_number) >= -2:
		guess = 0
	else:
		guess = 1
	#
	return guess


def find_same_number(ls):
	signal = ls[0]
	i = 1
	period = 0
	while i < len(ls):
		temp = ls[i]
		i += 1
		if temp == signal:
			period = i
			break;	
	return period
		


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
	k = gen_key(26)
	#
	# the cipher is queried with key k and message m[b]
# replace next line
	c = cycle_enigma_encipher(m[b],k)
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

# main

def parse_args():
	parser = argparse.ArgumentParser(description="The adversary protocol game for a enigma-type cipher.")
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
		print (cycle_enigma_encipher(args_g.argument, encode_alpha_key(args_g.keyword)))



if __name__ == "__main__":
	main(sys.argv)

