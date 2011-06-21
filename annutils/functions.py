import numpy, random, math

def set_diagonal(m, x = 0.):
	m.flat[::m.shape[1]+1] = x
	return m

def _pthresh(x, t = 1.):
	i = x*t
	if i < -45:
		return 0.
	if i > 45:
		return 1.
	if 1./(1.+math.exp(-i)) < random.random():
		return 0.
	return 1.

pthresh = numpy.vectorize(_pthresh)

def sigmoid(a):
	return 1./(1.+numpy.exp(-a))

