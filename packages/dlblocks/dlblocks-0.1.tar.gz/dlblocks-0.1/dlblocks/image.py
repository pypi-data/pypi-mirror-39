
import numpy as np
import cv2


import pyutils


IMG_WIDTH = 224
IMG_HIEGHT = 224

VGGIMG_SIZE = 224

import threading
lock = threading.Lock()

from tqdm import tqdm

def get_np_array_from_tar_object(tar_extractfl):
     '''converts a buffer from a tar file in np.array'''
     return np.asarray(
        bytearray(tar_extractfl.read())
        , dtype=np.uint8)


# FLAGS -> opencv read flag ( 0 for gray and 1 for color )
def readimgtar( fname , tarf , FLAGS=1):
    with lock:
        xx = tarf.extractfile( fname )
        return cv2.imdecode(
            get_np_array_from_tar_object(xx) , FLAGS )

def zipimread( fn  , zf  , FLAGS=1):
    data = zf.read( fn )
    img = cv2.imdecode(np.frombuffer(data, np.uint8), FLAGS )    
    return img


def read_img_h5( key , hf , FLAGS=1 ):
    return cv2.imdecode( np.array(hf[ key ] ) , FLAGS)


def get_nframes(  vid_name  ):
    cap = cv2.VideoCapture(  DATASET_PATH + "final_data/" + vid_name + ".mp4" )
    assert cap.isOpened()
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return n_frames


def load_video_frames( fn  , width=None , height=None , verbose=False ):

    cap = cv2.VideoCapture( fn )
    assert cap.isOpened() 
    frames = []
    
    if verbose:
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for _ in tqdm(range(n_frames)) :
            ret, frame = cap.read()
            if ret == True:
                if  not width is None: 
                    frames.append(  cv2.resize(frame   , (width , height ))  )
                else:
                    frames.append( frame )
            else: 
                break
    else:    
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                if  not width is None: 
                    frames.append(  cv2.resize(frame   , (width , height ))  )
                else:
                    frames.append( frame )
            else: 
                break
    cap.release()
    return  np.array(frames)



def yield_video_frames( fn  , width=None , height=None , verbose=False):

    cap = cv2.VideoCapture( fn )
    assert cap.isOpened() 
    frames = []
    
    
    if verbose:
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for _ in tqdm(range(n_frames)) :
            ret, frame = cap.read()
            if ret == True:
                if  not width is None: 
                    yield  cv2.resize(frame   , (width , height ))  
                else:
                    yield frame 
            else: 
                break
    else:
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                if  not width is None: 
                    yield  cv2.resize(frame   , (width , height ))  
                else:
                    yield frame 
            else: 
                break
    cap.release()




# crop coordinates -> [[x1,y1] , [x2,y2] ] 
def getImageVec(path  , width=IMG_WIDTH , height=IMG_HIEGHT , cropCoordinates=None ,   augment=False , augmentationSeed = None , imgNorm="sub_mean" , pipelineOrder=['crop' , 'augment' , 'resize' , 'norm'] , maintainAspectRatio=False , src_type='file' , src=None , ordering='th' , readMode=1 ):

#     print path
    if src_type == 'file':
        img = cv2.imread(path, readMode)
    elif src_type == 'zip':
        img = zipimread(path , src , readMode )
    elif src_type == 'tar':
        img = readimgtar(path , src , readMode )
    elif src_type == 'h5':
        img = read_img_h5(path , src , readMode )
    elif src_type == 'np':
        img = path

    for fn in pipelineOrder:

        if fn == 'crop':
            if  not cropCoordinates is None:
                [[x1,y1] , [x2,y2] ] = cropCoordinates
                [[x1,y1] , [x2,y2] ]  = [[int(x1),int(y1)] , [int(x2),int(y2)] ]  
                pts1 = np.float32([ [x1 , y1 ] , [x2, y1] , [x1 , y2] , [x2 , y2] ])
                pts2 = np.float32([[0,0],[abs(x2-x1),0],[0,abs(y2-y1)],[abs(x2-x1),abs(y2-y1)]])
                M = cv2.getPerspectiveTransform(pts1,pts2)
                img = cv2.warpPerspective(img,M,(abs(x2-x1) , abs(y2-y1)  ))

        if fn == 'augment':
            if augment:
                import Augmentation
                img = Augmentation.augmentCVImage( img , augmentationSeed )

        if fn == 'resize' and ( not width is None ):
            if maintainAspectRatio:
                img_container = np.zeros((  height , width  , 3 ))
                h = np.size(img, 0)
                w = np.size(img, 1)
                ratio = (w+0.0)/h
                c1 = ( width ,  int( (width+0.0)/ratio   ) )
                c2 = ( int(height*ratio) , height   )
                if (c1[0] <= width and c1[1] <= height):
                    img = cv2.resize(img, c1 )
                else:
                    img = cv2.resize(img, c2 )
                img_container[0:0+img.shape[0], 0:0+img.shape[1]] = img
                img = img_container
            else:
                img = cv2.resize(img, ( width , height ))

        if fn == 'norm':
            if imgNorm == "sub_and_divide":
                img = np.float32( img ) / 127.5 - 1
            elif imgNorm == "sub_mean":
                img = img.astype(np.float32)
                img[:,:,0] -= 103.939
                img[:,:,1] -= 116.779
                img[:,:,2] -= 123.68
            elif imgNorm == "sub_mean_2":
                img = img.astype(np.float32)
                img  -= 128.0
            elif imgNorm == "divide":
                img = img.astype(np.float32)
                img = img/255.0

    if len( img.shape ) == 2: 
        img = img.reshape( tuple( list( img.shape ) + [1] ))

    if ordering == 'th':
        img = np.rollaxis(img, 2, 0)
    elif ordering == 'tf':
        img = img 

    return img





def getImagesVec(paths , stride=None , n_frames=None , **ka ):
    frames = []
    
    if type( paths ) is str or type( paths ) is unicode:
        paths = load_video_frames( paths )
        ka['src_type'] = 'np'
        
    for p in paths:
        frames.append( getImageVec(p , **ka ) )
        
    if not stride is None:
        frames = frames[::stride]
    elif not n_frames is None:
        new_frames = []
        for i in range( n_frames ):
            new_frames.append( frames[ int( (i*len(frames)*1.0)/float(n_frames) ) ])
        frames = new_frames
    return np.array(frames)




def getImageClassificationVec( d , baseImagePath , nClasses , width=IMG_WIDTH , height=IMG_HIEGHT , augment=False , augmentationSeed = None , imgNorm="sub_mean" , maintainAspectRatio=False ):

    return (getImageVec( baseImagePath + d['img'] , width=width , height=height , augment=augment , augmentationSeed=augmentationSeed , imgNorm=imgNorm , maintainAspectRatio=maintainAspectRatio ) 
        , pyutils.oneHotVec(d['classId'] , nClasses ) )



def getImageMulticlassClassificationVec( d , baseImagePath , nClasses , width=IMG_WIDTH , height=IMG_HIEGHT , augment=False , augmentationSeed = None , imgNorm="sub_mean" , maintainAspectRatio=False ):

    return (getImageVec( baseImagePath + d['img'] , width=width , height=height , augment=augment , augmentationSeed=augmentationSeed , imgNorm=imgNorm , maintainAspectRatio=maintainAspectRatio ) 
        ,General.getMultiClassificationVector(d['classIds'] , nClasses ) )




