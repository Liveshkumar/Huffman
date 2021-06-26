#!/usr/local/bin/python3
import sys
import argparse

class node:
    def __init__(self,char,freq,left=None, right=None):
        self.char= char
        self.freq= freq
        self.left= left
        self.right= right
        self.code=''

encode_bit={}
def generate_bit(node, val=''):
	bit = val + str(node.code)
	if(node.left):
		generate_bit(node.left, bit)
	if(node.right):
		generate_bit(node.right, bit)
	if(not node.left and not node.right):
		encode_bit[node.char]=bit
		
def get_encode(txt):
	encode_text=""
	for i in txt:
		encode_text+=(encode_bit[i])
		#print(i,encode_bit[i],end=" ")
	return encode_text
def padding(encoded_txt):
	extra_pad=8-len(encoded_txt)%8
	#print(extra_pad)
	for i in range(extra_pad):
		encoded_txt += "0"
	padding_val="{0:08b}".format(extra_pad)
	encoded_txt=padding_val+encoded_txt
	return encoded_txt
# get frequency of char function
def get_frequency(text):
	freq={}
	for i in text:
		if i not in freq:
			freqi]=0
		freq[i]+=1
	return freq
def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	file1 = open(input_file,"r")
	text=file1.read()
	freq=get_frequency(text)
	BST=[]
	for i in freq:
		BST.append(node(i,freq[i]))
	while(len(BST)>1):
		nodes = sorted(BST, key=lambda x: x.freq)
		left=nodes[0]
		right=nodes[1]
		left.code=0
		right.code=1
		newNode = node(left.char+right.char,left.freq+right.freq,  left, right)
		BST.remove(left)
		BST.remove(right)
		BST.append(newNode)

	generate_bit(BST[0])

	encode_text=get_encode(text)
	#print(encode_text)
	encoded_txt=padding(encode_text)
	#print(len(encoded_txt)%8)
	characters = ""
	for i in range(0, len(encoded_txt), 8):
		char_int = int(encoded_txt[i:i+8], 2)
		#print(char_int,end=" ")
		characters += chr(char_int+1)
	decode_dict={}
	for i in encode_bit:
		decode_dict[encode_bit[i]]=i
	# storing length of encode bit + encode bit values + encoded chars
	file3=open("decode.txt",'w')
	file3.write(str(decode_dict))
	file2=open(output_file,'w')
	file2.write(characters)
	file2.close()
	file1.close()

# deocde functions	
def get_padding_val(text):
	char=ord(text[0])
	pad_val=int(char)
	#print(pad_val)
	return pad_val
def decode_char(text):
	decode_text=""
	for i in text:
		char=ord(i)-1
		c="{0:08b}".format(char)
		decode_text+=c
	return decode_text
def removed_padding(decode_text,padval):
	decode_text=decode_text[:-1*padval]
	return decode_text

def decode_huffambit(decode_text,decode_dict):
	ch=""
	encode_char=""
	for i in decode_text:
		ch+=i
		if ch in decode_dict:
			encode_char+=decode_dict[ch]
			ch=""
	return encode_char

def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	file1=open(input_file,'r')
	file2=open(output_file,'w')
	file3=open("decode.txt",'r')
	dict1=file3.read()
	text=file1.read()
	dict1=eval(dict1)
	pad_val=get_padding_val(text)
	decode_text=decode_char(text[1:])
	decode_text=removed_padding(decode_text,pad_val)
	encode_char=decode_huffambit(decode_text,dict1)
	file2.write(encode_char+'\n')
	file2.close()
	file3.close()
	file1.close()


def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options


if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)

		
