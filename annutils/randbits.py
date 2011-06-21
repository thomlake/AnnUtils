#---------------------------------------#
#	This file is part of AnnUtils.
#
#	AnnUtils is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	AnnUtils is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with AnnUtils.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------#
# author:
#	tllake 
# email:
#	<thomas.l.lake@wmich.edu>
#	<thom.l.lake@gmail.com>
# date:
#	2011.06.28
# file:
#	randbits.py
# description:
#	functions for probabilistically creating,
#	degrading (changing some 1's to 0's), and 
#	mutating (flipping random bits) binary
#	lists or numpy arrays.
#
#	class for storing and retrieving random representations
#	of data.
#---------------------------------------#
import random
import numpy

ON = 1
OFF = 0

def bnot(x, on = ON, off = OFF):
	"""return the not of x.
	
	:param x: the value to not
	:param on: true
	:param off: false
	:type x: any
	:type on: any
	:type off: any
	"""
	if x == on:
		return off
	return on

def pflip(x, p, on = ON, off = OFF):
	"""flip x with probability p
	
	:param x: the value to flip, potentially
	:param p: the probability of x being flipped
	:param on: true
	:param off: false
	:type x: any
	:type p: float
	:type x: any
	:type x: any
	"""
	if random.random() < p:
		return bnot(x, on, off)
	return x

def gen(n, p_on = 0.5, on = ON, off = OFF, np = False):
	"""generate a random list or numpy.ndarray of binary(ish) values.

	:param n: length of returned iterable
	:param p_on: probability that any element is on
	:param on: true
	:param off: false
	:param np: if True return a numpy array
	:type n: int
	:type p_on: float
	:type on: any
	:type off: any
	:type np: boolean
	"""
	b = [on if random.random() < p_on else off for i in range(n)]
	if np:
		return numpy.array(b)
	return b

def mutate(bits, p_change = 0.2, on = ON, off = OFF):
	"""return a noisy copy of bits.
	:param bits: the iterable to mutate
	:param p_change: probability that any bit in bits is flipped
	:param on: true
	:param off: false
	:type bits: list or numpy.ndarray
	:type p_change: float
	:type on: any
	:type off: any
	"""
	if type(bits) is numpy.ndarray:
		newbits = numpy.array([pflip(x, p_change, on, off) for x in bits])
	elif type(bits) is list:
		newbits = [pflip(x, p_change, on, off) for x in bits]
	else:
		raise TypeError('type(bits) must be list or numpy.ndarray')
	return newbits

def degrade(bits, p_change = 0.2, on = ON, off = OFF):
	"""same as mutate but only on values are potentially changed.
	
	:param bits: the iterable to degrade
	:param p_change: probability that any on bit in bits is off
	:param on: true
	:param off: false
	:type bits: list or numpy.ndarray
	:type p_change: float
	:type on: any
	:type off: any
	"""
	if type(bits) is numpy.ndarray:
		newbits = numpy.array([pflip(x, p_change, on, off) if x == on else x for x in bits])
	elif type(bits) is list:
		newbits = [pflip(x, p_change, on, off) if x == on else x for x in bits]
	else:
		raise TypeError('type(bits) must be list or numpy.ndarray')
	return newbits

def bitstr(bits, on = ON, off = OFF, onsymbol = '+', offsymbol = '-'):
	"""return a string representation of bits.

	:param bits: iterable to change to string
	:param on: true
	:param off: false
	:param onsymbol: character representation of on
	:param offsymbol: character representation of off
	:type bits: list or numpy.ndarray
	:type on: any
	:type off: any
	:type onsymbol: chr
	:type offsymbol: chr
	"""
	return ''.join([onsymbol if x == on else offsymbol for x in bits])

class RandomRepresentation(object):
	"""class for handling data representations as random
	binary lists or numpy.ndarray

	:param n: length of representaion
	:param p_on: probability the a bit is set in the representation
	:param on: true
	:param off: false
	:param np: if True use numpy.ndarray
	:param alphabet: keys
	:type n: int
	:type p_on: float
	:type on: any
	:type off: any
	:type np: boolean
	:type alphabet: iterable of hashables
	"""
	def __init__(self, n, p_on=0.5, on=ON, off=OFF, np=False, alphabet=None):
		self.n = n
		self.p_on = p_on
		self.on = on
		self.off = off
		self.np = np
		self.io = dict()
		self.oi = dict()
		if not alphabet is None:
			self.add_alphabet(alphabet)

	def keyof(self, val):
		"""return the key associated with a representation.
		
		:param val: a representation
		:type val: iterable
		"""
		return self.oi[bitstr(val)]

	def valof(self, key):
		"""return the representation for key.

		:param key: data
		:type key: hashable
		"""
		return self.io[key]

	def add_alphabet(self, alphabet):
		"""create a representation for all items in alphabet.

		:param alphabet: contains data points
		:type alphabet: iterable of hashables
		"""
		for letter in alphabet:
			self.add(letter)

	def add(self, key):
		"""create unique representation for key.

		:param key: data
		:type key: hashable
		"""
		if key not in self.io:
			val = gen(self.n, self.p_on, self.on, self.off, self.np)
			while bitstr(val) in self.oi:
				val = gen(self.n, self.p_on, self.on, self.off, self.np)
			self.io[key] = val
			self.oi[bitstr(val, self.on, self.off)] = key

if __name__ == '__main__':
	# test
	sigma = 'abcdefg'
	n = 10
	p_on = 0.3
	#a = gen(n, p_on, np = True)
	#print a, bitstr(a)
	rr = RandomRepresentation(n = n, p_on = p_on, alphabet = sigma, np = True)
