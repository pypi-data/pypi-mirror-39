
import numpy as np  
import json 
from tqdm import tqdm 
import os 

# from Utils.PyUtils import mapArrays , loadJson , saveJson , oneHotVec , makeGenerator

def set_gpu( gpu_id ):
    import os
    os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)

    
    
# load a json
def loadJson( fname ):
    return json.loads( open(fname).read() )

# save a json
def saveJson( fname , data ):
    open( fname , 'wb').write( json.dumps(data) )

# run map operator and return structure of arrays
# if could return dict of arrays , list of arrays .. etc
def mapArrays( data , func , *args, **kwargs  ):

    L = None
    for d in tqdm( data ) :
        mapped =  func( d , *args, **kwargs) 

        if L is None:
            if type(mapped) is list :
                L = [ [] for _ in len( mapped )  ]
            elif type(mapped) is tuple:
                L = tuple( [ [] for _ in len( mapped )  ])
            elif type(mapped) is dict:
                L = { key : [] for key in mapped.keys()}

            else:
                L = []

        if type(mapped) is list or  type(mapped) is tuple:
            if any( map( (lambda x: x is None ) , mapped )):
                continue
            for i , m in enumerate( mapped ):
                L[i].append( m )
        elif type(mapped) is dict:
            for key in mapped.keys():
                L[key].append( mapped[key] )
        else:
            L.append( mapped )
            
            
    if type( L ) is dict:
        for k in L.keys():
            L[k] = np.array(L[k])
    else:
        L = map( np.array , L )

    return L 


# make a one hot numpy vector of a class
def oneHotVec( classId , nClasses ):
    v = np.zeros( nClasses )
    v[classId] = 1
    return v			

# reterun a tuple of list OR a list where it selects keys from dict of list
def selectKeys( items ,  keys ):

    if type(keys) is list or  type(keys) is tuple:
        LL = []
        for key in keys :
            l = [ x[key] for x in items ]
            LL.append( l )

        if type(keys) is tuple:
            LL = tuple( LL )
        return LL 
    else:
        key = keys 
        return [ x[key] for x in items ]




# pad a list
# el -> element to pad with
def padList( inp , maxLen , el=0 , side='right'  ):
    if side == 'right':
        inp = inp[:maxLen]
    else:
        inp = inp[-1*maxLen:]

    if len(inp) < maxLen:
        if side == 'right':
            inp = inp + [el]*(maxLen - len(inp) )
        else:
            inp =  [el]*(maxLen - len(inp) ) + inp

    return inp


def int64Arr( d ):
    return np.array( d ).astype('int64')


def floatArr( d ):
    return np.array( d ).astype('int64')


def env_arg( key , default=None , type=str ):
    key = str( key )
    
    if type is bool:
        type = lambda x : bool( int( x ))
    
    if key in os.environ:
        r = type( os.environ[key] )
        print key , "->" , r 
        return r
    else:
        if not default is None :
            r = default
            print key , "->" , r , "(default)"
            return r 
        else:
            raise Exception( key + ' Not found')

def makeGenerator( data ):
    for d in data:
        yield d
        
        
def mapGenerator( fn , g ):
    for d in g:
        yield fn( d )
        
        

def loadJsonAppend( fname ):
    import ijson
    import subprocess
    read_process = subprocess.Popen( 'echo "[";  cat "%s" | head -c -2   ; echo "]" '%fname   , shell=True , stdout=subprocess.PIPE)
    FF = ijson.items( read_process.stdout  , "item")
    for item in FF:
            yield item


