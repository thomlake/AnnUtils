import numpy, random, math

def set_diagonal(m, x = 0.):
	m.flat[::m.shape[1]+1] = x
	return m

def _pthresh(x):
	if x < random.random():
		return 0.
	return 1.

pthresh = numpy.vectorize(_pthresh)

def sigmoid(a, t = None):
	if t is None:
		return 1./(1.+numpy.exp(-a))
	return 1./(1.+numpy.exp(-t*a))

def tanh(a, t = None):
	if t is None:
		return numpy.tanh(a)
	return numpy.tanh(t*a)

def _stateful(x, i):
	if x < 0.:
		# x just fired, refractory period
		return 0., 0.

	a = x + i

	if a < 0.:
		# x is being inhibited
		return 0., 0.
	a = 1/(1+math.exp(-a))
	if a < random.random():
		return 0., a
	return 1., -1.

stateful = numpy.vectorize(_stateful)

