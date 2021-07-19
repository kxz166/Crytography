import string
import sys
import os
import argparse

from Proj4 import Padding_Oracle

#
# padding-attack.py
#
# author:Kerui Zeng
# date: 10.25.2019
# last update:11.4.2019
#
# template by: bjr oct 2019
# template update: 22 oct 2019
#

args_g = 0  # args are global
	
BLOCK_SIZE = 16


def attack_mode(oracle, intext):
	
	outtext = bytearray()
	remove_paading_outtext = bytearray()
	faketext = b""
	fakeintext = bytearray(BLOCK_SIZE*2)
	
	padding_value = 0
	block_message = bytearray(BLOCK_SIZE)
	temptext = bytearray(BLOCK_SIZE*2)

	block_list = split_into_block_list(intext)
	lens = len(block_list)

	output_list = [bytearray(BLOCK_SIZE) for _ in range(lens-1	)]
	#print("This is block_list#1:", block_list)
	CopyList = split_into_block_list(intext)
	fake_block = CopyList[0]

	#print("THis is lens of block_list", len(block_list[-1]))

	for i in range(0, 16): 
		fake_block[i] = i
		# print(fake_block)
		faketext += fake_block

		for j in range(1, lens):
			faketext += block_list[j]

		fake_result = bytearray(faketext)
		# print(fake_result)
		if (oracle.padding_oracle(fake_result) == False):
			padding_value = BLOCK_SIZE - i
			#print(padding_value)
			break
		faketext = b""
	
	value_for_removing = padding_value


	#print("#2:", block_list)		problem is here

	delta = bytearray(BLOCK_SIZE)
	#print(intext)
	#print(oracle.decrypt_only(intext))
	
	for i in range(len(block_list)-1,0,-1):
		#print("This is first block_list:", block_list)
		temptext[:BLOCK_SIZE] = block_list[i-1]
		#print("This is firt temptext:",temptext)
		temptext [BLOCK_SIZE:]= block_list[i]
		#print("This is temptext: ",temptext)
		#print("#1: ", len(temptext))
		if i != len(block_list) - 1:
			padding_value = 0
		#print("This is padding value: ",padding_value)
		#print("#1: ", len(temptext))
		for j in range (BLOCK_SIZE*2):
			fakeintext[j] =temptext[j]
		#print("This is fakeintext: ",fakeintext)
		#print("This is block_message",block_message)
		#print("#1: ", len(temptext))
		output_list[i-1] = (findBlock(oracle,fakeintext,delta,temptext,padding_value))	
	for i in range(len(output_list)):
		outtext += output_list[i]
	
	
	#print(value_for_removing)
	#print("This is outtext: ",outtext)
	if value_for_removing != 0:
		remove_paading_outtext = outtext[:len(outtext)-value_for_removing]
	elif value_for_removing == 0:
		for i in range(len(output_list)-1):
			remove_paading_outtext += output_list[i]
	print("This is ByteArray result: ",remove_paading_outtext)



def findBlock(oracle,fakeintext,delta,intext,padding_value):
	message = bytearray(BLOCK_SIZE)
	for i in range(BLOCK_SIZE):
		delta[i] = 0
	#print("THis is delta: ",delta)
	new_padding_value = padding_value + 1 
	
	#print(delta)
	#print("This is padding_value: ",padding_value)
	# do in one block:
	#print("#1: ",len(intext))
	start_point = BLOCK_SIZE-padding_value-1
	#print(start_point)
	for i in range(start_point,-1,-1):
		message[i] = findM(oracle,fakeintext,delta,intext,padding_value,new_padding_value,message)
		#print("This is message: ",message)
		#initial fakeintext
		for j in range (len(intext)):
			#print("This is J: ",j)
			#print("This is len of f: ",len(fakeintext))
			#print("This is len of inte: ",len(intext))
			fakeintext[j] =intext[j]
		new_padding_value += 1

	return message	
		
		
		


def findM(oracle,fakeintext,delta,intext,padding_value,new_padding_value,message):
	m = 0
	#print("This is intext: ",intext)
	#print("this is decrpyt:", oracle.decrypt_only(intext))
	#print("This is fakeintext: ", fakeintext)

	if padding_value < BLOCK_SIZE:
		
		for i in range((BLOCK_SIZE - padding_value), BLOCK_SIZE):
			delta[i] = (new_padding_value) ^ (padding_value)
		for i in range(BLOCK_SIZE - padding_value-1,BLOCK_SIZE-new_padding_value,-1):
			delta[i] = (message[i]^(new_padding_value))
			#print("this is a after4 delta ",delta)
		#print("This is delta: ",delta)
		for i in range(0, 256):
		
			delta[BLOCK_SIZE - new_padding_value] = i
			#print("this is changing delta  ",delta)
			fakeintext[:BLOCK_SIZE] = xor(intext[:BLOCK_SIZE], delta)
			#print("this is fakeintext,   " ,fakeintext)
			#print(oracle.decrypt_only(fakeintext))
			if oracle.padding_oracle(fakeintext):
				#print("success")	
				#print('THIS IS PADDING +1: ',padding_value+1)
				#print("THIS IS i: ",i)
				m = i^((new_padding_value))
			#initial fakeintext
				#break
				#print("This is M:", m)
	
	return m


def xor(ciphertext,plaintext):
	buf = bytearray(BLOCK_SIZE)
	for i in range(BLOCK_SIZE):
		buf[i] = plaintext[i] ^ ciphertext[i]
	return buf


def split_into_block_list(intext):
	block_list = []

	for i in range(0, len(intext), BLOCK_SIZE):
		block_list.append(intext[i:i + BLOCK_SIZE])

	return block_list


def encrypt_mode(oracle, intext):
	outtext = oracle.encrypt(intext)
	sys.stdout.buffer.write(outtext)


def decrypt_mode(oracle, intext):
	outtext = oracle.decrypt(intext)
	sys.stdout.buffer.write(outtext)

	
# first one on the list is the default
modes = ["encrypt", "decrypt", "attack"]
# callout table
modes_f = {"encrypt": encrypt_mode, "decrypt": decrypt_mode, "attack": attack_mode}


def parse_args():
	parser = argparse.ArgumentParser(description="Padding attack against ciphertext from stdin. ")
	parser.add_argument("key", help="encipherment key, for oracle use only")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	parser.add_argument("-m", "--mode", help="mode either encrypt, decrypt, or attack")
	parser.add_argument("-R", "--norandomness", action="store_true",
						help="set IV and key to zero (key argument required but ignored)")
	parser.add_argument("-z", "--zero", action="store_true", help="use zeros padding")
	return parser.parse_args()


def main(argv):
	global args_g
	args_g = parse_args()
	if args_g.mode not in modes:
		args_g.mode = modes[0]

	padding_oracle = Padding_Oracle(key=args_g.key, zero_padding=args_g.zero,
									norandomness=args_g.norandomness)
	bintext = bytearray(sys.stdin.buffer.read())
	modes_f[args_g.mode](padding_oracle, bintext)


main(sys.argv)
