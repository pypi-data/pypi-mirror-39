

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools
import cv2
import random

def plotDictHisto( dictionay , outputFile ):
	pl = plt
	plt.clf()
	plt.cla()
	X = np.arange(len(dictionay))
	pl.bar(X, dictionay.values(), align='center', width=0.5)
	pl.xticks(X, dictionay.keys())
	pl.xticks(rotation=90)
	ymax = max(dictionay.values()) + 1
	pl.ylim(0, ymax)
	
	if not outputFile is None:
		plt.savefig( outputFile )
	else:
		plt.show()


def plotArr_mpl( arr  , outputFile=None   ):
	H = np.array( arr )  # added some commas and array creation code

	fig = plt.figure(figsize=(6, 3.2))

	ax = fig.add_subplot(111)
	ax.set_title('colorMap')
	plt.imshow(H)
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(0)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	
	
	if not outputFile is None:
		plt.savefig( outputFile )
	else:
		plt.show()


# # plots a descrete 2d array with value on each cell!
def plotArr_mpl_withVals( arr  , outputFile=None   ):

	cm = arr
	plt.clf()
	plt.imshow(cm, interpolation='nearest' )
	# plt.title(title)
	plt.colorbar()

	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i, j],
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()

	if outputFile is None:
		plt.show()
	else:
		plt.savefig( outputFile )
	plt.clf()




def plotImageMask( img , arr , outputFile=None   ):

	arr =arr*255
	img2  = cv2.applyColorMap(arr , cv2.COLORMAP_JET)
	cv2.imwrite( outputFile , img2 )
	im_gray = cv2.imread(outputFile, cv2.IMREAD_GRAYSCALE)
	im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)

	img = cv2.imread( img )
	height, width, channels = im_color.shape
	img = np.float32(cv2.resize(img, ( width , height )))
	avg = (img + im_color)/2
	cv2.imwrite( outputFile , avg )



# this one doesnt change the main image size but it will resize the CN acodigly
def plotImageMask_2( img , arr , outputFile=None   ):

	arr =arr*255
	img2  = cv2.applyColorMap(arr , cv2.COLORMAP_JET)
	cv2.imwrite( outputFile , img2 )
	im_gray = cv2.imread(outputFile, cv2.IMREAD_GRAYSCALE)
	im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)

	img = cv2.imread( img )
	height, width, channels = img.shape
	im_color = np.float32(cv2.resize(im_color, ( width , height )))
	avg = (img + im_color)/2
	cv2.imwrite( outputFile , avg )



# this one just highlights the importang regions
# like we do in cam
def plotImageMask_3( img , arr , outputFile=None , thesh = 0.2   ):

    original_img = cv2.imread(img )  
    width, height, _ = original_img.shape
    cam = np.copy(arr)
    cam -= np.min(cam) 
    cam /= np.max(cam)
    # cam = cv2.resize(cam, (14, 14) , interpolation=cv2.INTER_NEAREST  )
    cam = cv2.resize(cam, (height, width)   )
    
    cam -= thesh
    cam /= (1-thesh)
    cam[np.where(cam < 0)] = 0
    heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
    heatmap[np.where(cam < 0.2 )] = 0
    img = heatmap*0.5 + original_img
    
    cv2.imwrite( outputFile , img )

    


def plotArr2( arr  , outputFile=None   ):
	x , y = range(arr.shape[1]) , range(arr.shape[0])
	x, y = np.meshgrid(x, y)

	plt.pcolormesh(x, y, arr )

	if not outputFile is None:
		plt.savefig( outputFile )
	else:
		plt.show()

def plotArr( arr  , outputFile=None   ):

	arr =arr*255

	img2  = cv2.applyColorMap(arr , cv2.COLORMAP_JET)
	cv2.imwrite( outputFile , img2 )
	im_gray = cv2.imread(outputFile, cv2.IMREAD_GRAYSCALE)
	im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)
	cv2.imwrite( outputFile , im_color )




# http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix( confusion_matrix, classes=None,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues , outputFile=None ):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	cm = confusion_matrix
	cm = np.array(cm)

	if classes is None:
		classes = range( cm.shape[0] )

	plt.clf()
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	print(cm)

	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i, j],
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')

	if outputFile is None:
		plt.show()
	else:
		plt.savefig( outputFile )
	plt.clf()



def plot_confusion_matrix_2(cm , labels=None , fname=None ):
    conf_arr = cm
    norm_conf = []
    for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)

    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
                    interpolation='nearest')
    conf_arr = np.array(conf_arr)

    width, height = conf_arr.shape
#     print "h" , height
#     for x in xrange(width):
#         for y in xrange(height):
#             ax.annotate(str(conf_arr[x][y]), xy=(y, x), 
#                         horizontalalignment='center',
#                         verticalalignment='center')

#     cb = fig.colorbar(res)

    if labels is None:
        labels = ['']*height

    assert( len(labels) == height )
    import matplotlib
    matplotlib.rcParams.update({'font.size': 220/height })


    alphabet = labels
    # plt.xticks(range(width), alphabet[:width])
    plt.yticks(range(height), alphabet[:height] , fontsize=220/height  )
    plt.savefig(fname)



def display_frames_as_gif(frames):
    import matplotlib.pyplot as plt
    from JSAnimation.IPython_display import display_animation
    from matplotlib import animation
    from IPython.display import display

    """
    Displays a list of frames as a gif, with controls
    """
    #plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi = 72)
    patch = plt.imshow(frames[0])
    plt.axis('off')

    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames = len(frames), interval=50)
    display(display_animation(anim, default_mode='loop'))
    


    
def play_vid( fname ):
    import io
    import base64
    from IPython.display import HTML

    video = io.open(fname , 'r+b').read()
    encoded = base64.b64encode(video)
    return HTML(data='''<video alt="test" controls>
                    <source src="data:video/mp4;base64,{0}" type="video/mp4" />
                 </video>'''.format(encoded.decode('ascii')))

from tqdm import tqdm

def dump_video_from_np(fn , frames , verbose=False ):
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter( fn , fourcc , 20.0, ( frames.shape[2] ,frames.shape[1]))
    if verbose:
        for fr in tqdm(frames):
            out.write(fr)
    else:
        for fr in frames:
            out.write(fr)
    out.release()

def play_vid_np( frames ):
    fn = "/tmp/%d.mp4"%(random.randint(0,1000000009))
    dump_video_from_np(fn , frames , verbose=False )
    return play_vid( fn )


# m = [[33, 0, 0, 2, 0, 0, 0, 0, 0, 0],
#  [ 5, 5, 1, 3, 3, 0, 2, 0, 0, 0],
#  [ 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
#  [ 4, 4, 3, 4, 0, 1, 1, 0, 0, 0],
#  [ 0, 0, 1, 1, 7, 0, 0, 1, 0, 0],
#  [ 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
#  [ 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
#  [ 0, 0, 0, 0, 0, 0, 1, 3, 0, 0],
#  [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#  [ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

# m = [[34,0,0,1,0,0,0,0,0,0],
#  [ 0 ,13,3,0,1,0,1,1,0,0],
#  [ 0,0,3,0,0,0,0,0,0,0],
#  [ 0, 15,0,2,0,0,0,0,0,0],
#  [ 0,0,0,0,9,0,1,0,0,0],
#  [ 0,3,0,0,0,2,0,0,0,0],
#  [ 0,0,1,0,0,0,3,0,0,0],
#  [ 0,2,0,0,0,0,0,2,0,0],
#  [ 0,0,0,0,0,1,0,0,0,0],
#  [ 0,0,0,0,0,0,0,0,0,1]]

# plot_confusion_matrix( m )

