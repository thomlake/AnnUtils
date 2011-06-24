from PIL import Image
import numpy as np

def colorscale(x, color = 'grey'):
	if color == 'grey':
		return (0xff000000 + (x<<16) + (x<<8) + x)
	if color == 'red':
		return 0xff000000 + (x)
	if color == 'green':
		return 0xff000000 + (x<<8)
	if color == 'blue':
		return 0xff000000 + (x<<16)
	if color == 'dblue':
		return 0xff000000 + (64<<16) + (51<<8) + 37
npcolorscale = np.vectorize(colorscale)

def norm255(x, minval = 0., maxval = 1.):
	return np.array(255 * ((x - minval) / (maxval - minval)), dtype = np.uint32)


def drawpil(fname, imgdata):
	w,h = imgdata.shape
	imgdata.shape = h,w
	colordata = np.array(imgdata, copy=True, dtype=np.uint32) # HACK
	image = Image.frombuffer('RGBA', imgdata.shape, colordata, 'raw', 'RGBA', 0, 1)
	image.save(fname)

class PixelImageDrawer(object):
	def __init__(self, minval = 0., maxval = 1.):
		self.minval = minval
		self.maxval = maxval
		self.data = []

	def addrow(self, x, color = 'grey', minval = None, maxval = None):
		minval = self.minval if minval is None else minval
		maxval = self.maxval if maxval is None else maxval
		d = npcolorscale(norm255(x, minval, maxval), color)
		self.data.append(d)

	def addrowlist(self, l, color = 'grey', minval = None, maxval = None):
		minval = self.minval if minval is None else minval
		maxval = self.maxval if maxval is None else maxval
		for row in l:
			d = npcolorscale(norm255(row, minval, maxval), color)
			self.data.append(d)
	
	def draw(self, fname):
		drawpil(fname, np.vstack(self.data))

if __name__ == '__main__':
	# test
	pxlimg = PixelImageDrawer(0., 1.)
	for i in range(200):
		row = np.array([float(x) for x in '{0:b}'.format(i).rjust(100, '0')])
		pxlimg.addrow(row, color = 'grey')
	pxlimg.draw('test.png')

