import string
import sys
import os
import argparse
import random

from Bozhu_AES import AES

#
# encrypt.py
#
# author:
# date: 
# last update:
#
# template by: bjr sep 2019
# template update: 24 sep 2019
#

args_g = 0  # args are global

BLOCK_SIZE = 16  # the AES block size
KEY_SIZE = 16	# the AES key size


def run(aes,intext,):
	block_list = split_into_block_list(intext)
	if args_g.decrypt:

		return decryp(aes,block_list)
	else:
		block_list_after_padding = padding(block_list, BLOCK_SIZE)

	return decryp(aes,block_list_after_padding)

def split_into_block_list(intext):
	block_list = []

	for i in range(0, len(intext), BLOCK_SIZE):

		block_list.append(intext[i:i+BLOCK_SIZE])

	return block_list

def padding(block_list,BLOCK_SIZE):
	if args_g.padding == "zero":
		return zero_padding(block_list)
	elif args_g.padding == "pkcs":
		return pkcs_padding(block_list)
	elif args_g.padding == "iso":
		return  iso_padding(block_list)

def zero_padding(block_list):
	block_list[-1] =  (block_list[-1] + bytes(BLOCK_SIZE))[0:BLOCK_SIZE]
	return block_list

def	pkcs_padding(block_list):
	padding = b""
	if len(block_list[-1]) == BLOCK_SIZE:
		for i in range(BLOCK_SIZE):
			padding += bytes([BLOCK_SIZE])
		block_list.append(bytes(padding))
	else:
		rest = BLOCK_SIZE-len(block_list[-1])
		for i in range(rest):
			padding += bytes([rest])
		block_list[-1] = block_list[-1] + padding

	return block_list

def iso_padding(block_list):
	padding = b""
	padding += bytes([0x80])
	if len(block_list[-1]) == BLOCK_SIZE:
		for i in range(1,BLOCK_SIZE):
			padding += bytes([0x00])
		block_list.append(bytes(padding))
	else:
		rest = BLOCK_SIZE - len(block_list[-1])-1
		for i in range(rest):
			padding += bytes([0x00])
		block_list[-1] = block_list[-1] + padding

	return block_list



def xor(a,b):
	byte_list = []
	assert(len(a)==len(b))
	for i in range(len(a)):
		c = a[i] ^ b[i]
		byte_list.append(c)
	return bytes(byte_list)

def decryp(aes,block_list):
	if args_g.nonce == None:
		list = []
		for i in range(BLOCK_SIZE):
			random.seed(i)
			ran = random.random()
			nonce_one = int(ran * 255)
			list.append(nonce_one)
		args_g.nonce = bytes(list)

	if args_g.mode == "ecb":
		return ecb(aes,block_list)
	elif args_g.mode == "cbc":
		return cbc(aes,block_list,args_g.nonce)
	elif args_g.mode == "ofb":
		return ofb(aes,block_list,args_g.nonce)
	elif args_g.mode == "cntr":
		return cntr(aes,block_list,args_g.nonce)

def ecb(aes,block_list):
	outtext = b""

	if args_g.decrypt:
		for each in block_list:
			outtext += aes.decrypt_block(each)
		return unpadding(outtext)
	else:
		for each in block_list:

			outtext += aes.encrypt_block(each)


		return outtext

def cbc(aes,block_list,iv):

	crypt_list = []
	outtext = b""
	if args_g.decrypt:
		temp_bytes = aes.decrypt_block(block_list[0])
		temp_decrypt = xor(iv,temp_bytes)
		outtext += temp_decrypt
		for i in range(1,len(block_list)):
			temp_bytes =aes.decrypt_block(block_list[i])
			temp_decrypt = xor(block_list[i-1],temp_bytes)
			outtext += temp_decrypt

		return unpadding(outtext)
	else:

		first_bytes = xor(iv,block_list[0])
		temp_encrypt = aes.encrypt_block(first_bytes)
		outtext += temp_encrypt
		for i in range(1,len(block_list)):
			temp_bytes = xor(block_list[i],temp_encrypt)
			temp_encrypt = aes.encrypt_block(temp_bytes)
			outtext += temp_encrypt

		return outtext

def ofb(aes,block_list,iv):
	outtext = b""
	encrypt_iv = aes.encrypt_block(iv)
	encrypt_text = xor(encrypt_iv, block_list[0])
	outtext += encrypt_text
	for i in range(1, len(block_list)):
		encrypt_iv = aes.encrypt_block(encrypt_iv)
		encrypt_text = xor(encrypt_iv, block_list[i])
		outtext += encrypt_text

	if args_g.decrypt:
		return unpadding(outtext)


	return outtext

def cntr(aes,block_list,iv,):
	counter = 0;
	nonce = iv
	outtext = b""
	eiv = aes.encrypt_block(nonce)
	outtext += xor(eiv,block_list[0])
	for i in range(1,len(block_list)):
		counter += 1
		nonce = IvCounter(counter,len(block_list[i]))
		eiv = aes.encrypt_block(nonce)
		outtext += xor(eiv, block_list[i])

	if args_g.decrypt:
		return unpadding(outtext)

	return outtext

def IvCounter(counter,BLOCK_SIZE):
	run = counter*BLOCK_SIZE
	list = []
	for i in range(run,run+BLOCK_SIZE):
		random.seed(i)
		ran = random.random()
		nonce_one = int(ran*255)
		list.append(nonce_one)
	
	return bytes(list)

def unpadding(intext):
	outtext = b""
	index = 0
	if args_g.padding == 'pkcs':
		block_list = split_into_block_list(intext)
		num = block_list[-1][-1]
		block_list[-1] = block_list[-1][:(BLOCK_SIZE-num)]
		if num == BLOCK_SIZE:
			for i in block_list-1:
				outtext += i
		else:
			for i in block_list :
				outtext += i

	elif args_g.padding == "iso":

		for i in range(len(intext)):
			if intext[i] == 0x80:
				index = i
				break
		outtext = intext[0:index]
	elif args_g.padding == 'zero':
		index = 0
		block_list = split_into_block_list(intext)
		for i in range(len(block_list[-1])):
			if block_list[-1][i] == 00:
				index = i
				break
		block_list[-1] = block_list[-1][:index]
		for i in block_list:
			outtext += i
	return outtext










def parse_args():
	parser = argparse.ArgumentParser(description="Encrypt/decrypt stdin. ")
	parser.add_argument("key", help="encipherment key")
	parser.add_argument("-d", "--decrypt", action="store_true", help="decrypt, instead of encrypting")
	parser.add_argument("-m", "--mode", help="mode either cntr (default), cbc, ofb, or ecb")
	parser.add_argument("-n", "--nonce", help="the initial vector, as ascii. omit for a random nonce (recommended)")
	parser.add_argument("-p", "--padding", help="padding either pkcs (default), iso, or zero")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
	return parser.parse_args()

modes = ["cntr","cbc","ofb","ecb"]
pads = ["pkcs","iso","zero"]

def main(argv):

	global args_g
	args_g = parse_args()

	if args_g.mode not in modes:
		args_g.mode = modes[0]
	if args_g.padding not in pads:
		args_g.padding = pads[0]

	## check args
	if args_g.verbose:
		print("command line arguments-")
		print("\t-d:", args_g.decrypt)
		print("\t-m:", args_g.mode)
		print("\t-n:", args_g.nonce)
		print("\t-p:", args_g.padding)
		print("\t-v:", args_g.verbose)
		print("\tkey:", args_g.key)
	if args_g.key:
		key = [ord(i) for i in args_g.key]
		while len(key) < KEY_SIZE:
			key.append(0)
		aes = AES(bytes(KEY_SIZE))
	else:
		aes = AES(bytes(KEY_SIZE))
	try:
		bintext = sys.stdin.buffer.read()
		bintext = run(aes,bintext)
		sys.stdout.buffer.write(bintext)
	except Exception:
		pass


main(sys.argv)
