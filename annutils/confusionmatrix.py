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
#	confusionmatrix.py
# description:
#	class for counting and printing
# 	simultaneous occurence values of different 
# 	classes, i.e. a confusion matrix
#---------------------------------------#

class ConfusionMatrix:
	"""Class for counting and printing simultaneous occurence values of different classes.
	
	i.e. a confusion matrix.

	:param row_labels: prediction labels
	:param column_labels: actual labels
	:param padding: space between columns
	:type row_labels: list of strings
	:type column_labels: list of strings
	:type padding: int
	"""
	def __init__(self, row_labels, column_labels, padding = 12):
		self.padding = padding
		self.column_labels = column_labels
		self.row_labels = row_labels
		self.table = [[0.0]*len(column_labels) for i in range(len(row_labels))]

	def update(self, prediction, actual):
		"""Upate values in confusion matrix.

		:param prediction: row index
		:param actual: column index
		:type prediction: int
		:type actual: int
		:rtype: None
		"""
		self.table[prediction][actual] += 1

	def header(self):
		entry_template = '{0:^%d}|' %(self.padding)
		s = entry_template.format('')
		for label in self.column_labels:
			s += entry_template.format(label)
		s += '\n'
		return s

	def error(self, index = None):
		if index is None:
			return self.diagonal() / self.total()
		else:
			return self.table[index][index] / sum([table[i][index] for i in len(self.table)]) 

	def total(self):
		"""Calculate the total number of entries in the confusion matrix.
		
		:rtype: float
		"""
		return sum([sum(self.table[i]) for i in range(len(self.table))])

def diagonal(s:elf):
		"""Calculate the number of entires along the diagonal of the matrix.

		:rtype: float
		"""
		return sum([self.table[i][i] for i in range(len(self.table))])

	def error_tostring(self):
		"""Human readable error representation.

		:rtype: string
		"""
		tot = self.total()
		diag = self.diagonal()
		return 'accuracy: %0.02f, right: %0.02f, total: %0.02f\n' %(diag / tot if tot != 0 else 0.0, diag, tot)

	def data_row_string(self, i):
		"""Convert row i to a human readable string.

		:param i: the row to convert
		:type i: int
		:rtype: string
		"""
		entry_template = '{0:^%d}|' %(self.padding)
		s = entry_template.format(self.row_labels[i])
		for column_value in self.table[i]:
			s += entry_template.format(column_value)
		s += '\n'
		return s

	def tostring(self):
		"""Convert the Confusion Matrix to a human readable string.

		:rtype: string
		"""
		s = self.error_tostring()
		s += self.header()
		for i in range(len(self.row_labels)):
			s += self.data_row_string(i)
		return s

	def __str__(self):
		"""Convert the Confusion Matrix to a human readable string.

		:rtype: string
		"""
		return self.tostring()
