#!/usr/bin/python

'''
A simple python script to help me understand PIR better...
'''

import random
import math
import itertools

rand = random.random

def inline_print(n):
    return ''.join([str(_) for _ in n])

def random_bit():
    return random.getrandbits(1)

#Number of elements in the database. Fill it with random 0s and 1s
n = int(rand()*200)+10
elements = [random_bit() for i in range(n)]

print "The database (len=%s): " %n
print inline_print(elements)

#Index i (to be retrieved privately)
index_i = int(rand()*n)
print "Element to be retrieved at index i=%s" % index_i

#storing the actual value just to verify later
actual_val = elements[index_i]

sq_n = int(math.ceil(n**0.5))
#storing the row and column and then deleting the index_i
col = index_i%sq_n
row = index_i/sq_n
print "Index i=%s will occupy row=%s and col=%s in the %s x %s matrix." %(index_i, row, col, sq_n, sq_n)
del index_i

print ""

#pad zeros if the list isn't a perfect square. These won't be accessed anyway so it doesn't matter..
elements += [0]*(sq_n**2-len(elements))

'''
Represent [0,1,2,3,4,5,6,7,8] as shown below.
Note that 0..8 is the index
[[0,1,2],
[3,4,5],
[6,7,8]]
That is split the list into sqrt(n) * sqrt(n) lists and store it in two separate databases DB1 and DB2 that do not communicate
'''

DB1 = [list(i) for i in itertools.imap(None, *([iter(elements)]) * sq_n)]
DB2 = list(DB1)

print "Database DB1 (and DB2) in %sx%s format: " %(sq_n, sq_n)
for i in DB1:
    print inline_print(i)

#Random query Z1 made to DB1
Z1 = [random_bit() for i in range(sq_n)]

print ""
print "Z1 = %s" % inline_print(Z1)

#Only the column indices with '1' in Z1 will be considered when XOR sum is taken across the columns
A1 = []
for r in DB1:
    A1.append(sum([i&j for i,j in zip(r,Z1)])%2)
print "A1 = %s" % inline_print(A1)

#To compute Z2, flip the bit in col position
Z2 = list(Z1)
Z2[col] = Z2[col]^1

print ""
print "Z2 = %s" % inline_print(Z2)

#Z2 talks to DB2
#Now compute A2
A2 = []
for r in DB2:
    A2.append(sum([i&j for i,j in zip(r,Z2)])%2)
print "A2 = %s" % inline_print(A2)

#Compute A, which is the column containing the element at index_i. The desired element is at index 'row' in this list
A = [i^j for i,j in zip(A1,A2)]

print ""
print "A = %s\n" % inline_print(A)

required_element = A[row]
print "Required element: %s" % required_element
print "Verification: %s" %(required_element == actual_val)


