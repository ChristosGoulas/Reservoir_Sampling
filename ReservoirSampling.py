
#Christos Goulas
#A.M.=2677

import random
import re
from random import randint
import sys

l = int(sys.argv[1])
input_file = sys.argv[2]

#print K ( which is the size of the sample )  .
print( "k : " , l )

#print the input file that the user gave.
print( "input_file : " , input_file )

#print the initialized array
array = [None] * l
print( "----------------" )
print( "|  #\t| Line \t|" )
print( "----------------" )
for i in range(len(array)):
    print( "| " , ( i + 1 ) , "\t|" , array[i] , "\t|")
print("-----------------")


f = open(input_file)

#n is a counter for the stream objects - Here objects are lines  -
n = 0
counter = 0

for line in f:
	print("Incoming Line of Stream : ", line)
	n+=1
	print("N : ",n)
	if(n <= l):
		array [counter] = line
		counter += 1
		print( "----------------" )
		print( "|  #\t| Line \t|" )
		print( "----------------" )
		for i in range(len(array)):
			print( "| " , ( i + 1 ) , "\t|" , array[i])
		print("-----------------")
	else:
		print("n > K")
		print("We need to calculate propabilities p1 and p2.")
		p1=float(l/n)
		print("Propability (P1) K/n:",p1)
		p2=random.uniform(0,1)
		print("Random propability (P2) (propability to put in the sample the nth element ). Compare with K/n:",p2)
		if(p2>p1):
			print("P2>P1.We will not insert the new element")
			print( "----------------" )
			print( "|  #\t| Line \t|" )
			print( "----------------" )
			for i in range(len(array)):
				print( "| " , ( i + 1 ) , "\t|" , array[i])
			print("-----------------")
		else:
			print("P2<=P1.We will insert the new element")
			position=randint(0,l-1)
			print("Position to ovewrite",position)
			array[position]=line
			print( "----------------" )
			print( "|  #\t| Line \t|" )
			print( "----------------" )
			for i in range(len(array)):
				print( "| " , ( i + 1 ) , "\t|" , array[i])
			print("-----------------")
		