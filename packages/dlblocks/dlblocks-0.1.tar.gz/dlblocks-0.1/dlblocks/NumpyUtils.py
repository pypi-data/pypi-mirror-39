import numpy as np


def cutWindows( data ,  windowSizes , windowOffsets ):
	if type( data ) is list :
		data = np.array( data )
		isList = True 
		windowSizes = tuple(  [None] + list( windowSizes) )
		windowOffsets = tuple(  [None] + list( windowOffsets) )
	else:
		isList = False

	nDims = len( windowSizes )
	assert nDims == len( data.shape  )
	assert len( data.shape  ) == len( windowOffsets)

	