import numpy

def set_diagonal(m, x = 0.):
	m.flat[::m.shape[1]+1] = x
	return m

