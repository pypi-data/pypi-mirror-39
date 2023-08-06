


import numpy as np
import Images
import random
import cv2

IMG_WIDTH = 480
IMG_HIEGHT = 360



def getSegmentationAnnotationVec( path , nClasses ,  width=IMG_WIDTH , height=IMG_HIEGHT , augment=False , augmentationSeed = None , odering='flattened'  ):

	seg_labels = np.zeros((  height , width  , nClasses ))
	

	if path == "#na":
		seg_labels = np.reshape(seg_labels, ( width*height , nClasses ))
		return seg_labels

	try:
		img = cv2.imread(path, 1)

		if augment:
			import Augmentation
			img = Augmentation.augmentCVImage( img , augmentationSeed )


		img = cv2.resize(img, ( width , height ))
		img = img[:, : , 0]

		for c in range(nClasses):
			seg_labels[: , : , c ] = (img == c ).astype(int)

	except Exception, e:
		print e
	
	if odering == 'flattened':
		seg_labels = np.reshape(seg_labels, ( width*height , nClasses ))
		return seg_labels
	elif odering == 'channels_first':
		seg_labels = np.rollaxis(seg_labels, 2, 0)
		return seg_labels
	elif odering == 'img':
		return img.astype(np.int64 )

	




def getImageSegmentationVector( da , baseImagesPath  ,  nClasses , i_width=IMG_WIDTH  , i_height=IMG_HIEGHT   , o_width=IMG_WIDTH  ,o_height=IMG_HIEGHT , augment=False , augmentationSeed = None , imgNorm="sub_mean" , seg_odering='flattened' ):

	if augmentationSeed is None:
		augmentationSeed = random.randint( 0 , 100000 )

	x =  Images.getImageVec( baseImagesPath + da['img'] , width=i_width  , height=i_height ,  augment=augment , augmentationSeed = augmentationSeed , imgNorm=imgNorm )  
	y =   getSegmentationAnnotationVec( baseImagesPath + da['seg_annotation'] , nClasses , width=o_width , height=o_height ,  augment=augment , augmentationSeed = augmentationSeed , odering=seg_odering  ) 
	return x , y


