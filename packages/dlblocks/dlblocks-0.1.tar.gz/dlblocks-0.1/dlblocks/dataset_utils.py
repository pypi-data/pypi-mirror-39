import h5py
from  pyutils import makeGenerator , selectKeys
from tqdm import tqdm
import numpy as np


import numpy as np
from functools import partial
from threading import Thread
from multiprocessing import Pool


from misc import get_tqdm
tqdm = get_tqdm()


def parallizeGenerator( gen ):
    #
    queue = []
    #
    def worker():
        for X in gen:
            while( len(queue)) > 10:
                pass
            queue.append( X )
    #
    from threading import Thread
    t = Thread(target=worker, args=() )
    t.setDaemon(True )
    t.start()
    #
    while True:
        while len(queue) == 0:
            pass
        yield queue.pop(0)





def pMapTqdm( fn , lis , nProc=None, chunksize=1 ):
    p = Pool(processes=nProc )

    c = p.map_async( fn , lis, chunksize=chunksize )
    n = c._number_left # len(lis) # c._chunksize
    b = tqdm( total=n)
    while c._number_left>0:
        b.update( n -  c._number_left - b.n )
    b.update( n -  0 - b.n )
    return c.get()

# list l , chunksize - n
def get_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


# this function to be used by mapMakeH5DatasetParallel      
def procChunk(arg):
    fn , data , ind  = arg
    ret = {}
    for i,d in enumerate( data):
        mapped = fn( d )
        if i == 0:
            for key in mapped.keys():
                ret[key] = []
        for key in mapped.keys():
            ret[key].append( mapped[key] )
    for key in mapped.keys():
        saveFN = "/tmp/%d_%s.npy"%(ind , key)
        np.save( saveFN , np.array( ret[key] ) )
    del ret

# map a function to make a  h5 dataset , parallelly using VW
def mapMakeH5DatasetParallel( data , fn , h5f, length=None , nJobs=5 , chunkSize=1000) :
    if length is None:
        length = len( data )

    assert (length > 0)

    dataChunks = list( get_chunks( data , chunkSize )  )
    inds = range( len( dataChunks ) )   
    args = zip( [fn]*len( dataChunks) , dataChunks , inds )
    pMapTqdm( procChunk , args , nProc=nJobs ) 

    keys = fn( data[0]).keys()
    for key in keys:
        arr = np.load( "/tmp/%d_%s.npy"%(0 , key) )

        shape = tuple( [length] + list( arr[0].shape ) )
        dtype=arr[0].dtype
        h5f.create_dataset( key , shape , chunks=True , dtype= dtype )

    for key in keys:
        for i in inds:
            arr = np.load( "/tmp/%d_%s.npy"%( i , key) )
            h5f[key][i*chunkSize : (i+1)*chunkSize ] = arr




# map a function to make a  h5 dataset
def mapMakeH5Dataset( data , fn , h5f, length=None):
    if length is None:
        length = len( data )

    data = makeGenerator( data )

    for i in tqdm(  xrange( length ) ) :

        d = data.next()
        mapped = fn( d )

        if i == 0:
            for key in mapped.keys():
                shape = tuple( [length] + list( mapped[key].shape ) )
                dtype=mapped[key].dtype
                h5f.create_dataset( key , shape , chunks=True , dtype= dtype )

        for key in mapped.keys():
            h5f[key][i] = mapped[key]


def mapMakePyTablesDataset( data , fn ,h5f , length=None):

    import tables

    if length is None:
        length = len( data )

    if type( h5f) is str or type( h5f) is unicode:
        FILTERS = tables.Filters(complib=str('zlib'), complevel=5)
        h5file = tables.open_file( h5f , mode='w' , filters=FILTERS)

    arrays = {}

    vw = VectorizerWorker2( fn ,  data )
    gen = vw.dataPointVecGenerator()

    for i in tqdm(  xrange( length ) ) :

        mapped = gen.next()

        if i == 0:
            for key in mapped.keys():
                shape = list( [length] + list( mapped[key].shape ) )
                dtype = tables.Atom.from_dtype( mapped[key].dtype  )
                arrays[ key ] = h5file.create_carray( h5file.root, key , dtype,shape=shape)

        for key in mapped.keys():
            arrays[key][i] = mapped[key]

    if type( h5f) is str or type( h5f) is unicode:
        h5file.close()



def batchifyGenerator(dataPointVecGenerator , batchSize ):

    X = []
    Y = []

    Fusiom_XY_D = {}

    fusionXs = None
    fusionYs = None
    Fusiom_XY_D = None

    isFusionModelVec = False
    isFusionModelVecY = False
    fusionModelVecL = -1
    fusionModelVecLY = -1

    nDone = 0

    for d in  dataPointVecGenerator :
        
        if d is None:
            continue

        elif type (d) is dict :

            if Fusiom_XY_D is None:
                Fusiom_XY_D = {}
                for k in d.keys():
                    Fusiom_XY_D[k] = []

            for k in d.keys():
                Fusiom_XY_D[k].append( d[k]  )
            nDone += 1

            if nDone == batchSize:
                toYield = {}
                for k in d.keys():
                    toYield[k] = np.array( Fusiom_XY_D[k] )
                    Fusiom_XY_D[k]  = [] 
                nDone = 0

                yield toYield

        else:

            if type(d) is tuple and len( d ) == 2:
                x , y  = d
                justX = False
            else:
                x = d
                justX = True


            if type(x) is list or  type(x) is tuple:
                isFusionModelVec = True
                fusionModelVecL = len( x )
                if fusionXs is None:
                    fusionXs = [   []  for _ in range(fusionModelVecL)  ]

                for i in range( fusionModelVecL ):
                    fusionXs[i].append( x[i] )

            else:
                X.append(x)

            if not justX:
                if type(y) is list or  type(y) is tuple:
                    isFusionModelVecY = True
                    fusionModelVecLY = len( y )
                    if fusionYs is None:
                        fusionYs = [   []  for _ in range(fusionModelVecLY)  ]
                    for i in range( fusionModelVecLY ):
                        fusionYs[i].append( y[i] )

                else:
                    Y.append(y)

            nDone += 1

            if nDone == batchSize:
                if not isFusionModelVec:
                    yieldX =  np.array(X) 
                    X = []
                else:
                    yieldX =  [ np.array(fusionXs[i]) for i in range(fusionModelVecL)  ] 
                    fusionXs = [   []  for _ in range(fusionModelVecL)  ]

                if not justX:
                    if not isFusionModelVecY:
                        yieldY = np.array(Y)
                        Y = []
                    else:
                        yieldY =  [ np.array(fusionYs[i]) for i in range(fusionModelVecLY)  ] 
                        fusionYs = [   []  for _ in range(fusionModelVecLY)  ]

                nDone = 0

                if justX:
                    yield yieldX
                else:
                    yield yieldX , yieldY






class VectorizerWorker2():

    def __init__(self, vectorisationFn , data , batchSize=16 , nJobs=5 , datasize="small"):

        self.vectorisationFn = vectorisationFn
        self.data = data

        if datasize == "small":
            if type( data) is str or type( data) is unicode:
                if ".json" in data:
                    data = json.loads( open( data).read()  )
                else:
                    print "FILE FORMAT NOT SUPPORTED"

            self.data = list(data)
            assert len(self.data) > 0 
            self.totalDataPoints = len(data)
        else:
            self.totalDataPoints = None

        self.batchSize = batchSize
        self.nJobs = nJobs

        self.defaultGen = self.batchGenerator()

    def getNext( self ):
        return self.defaultGen.next()

    def reset( self ):
        self.defaultGen = self.generator()

    def getDataEntries(self):
        while True:
            for d in self.data:
                yield d

    def getDataEntriesBatch(self , batchSize):
        gen = self.getDataEntries()
        while True:
            yield [ gen.next() for i in range(batchSize)  ]


    # this takes some bunch of data points to vectorize and vectorizes them and append them in the dest !
    def vectorizeInBG( self, batch ,  dst ):

        def do():
            for d in batch:
                dst.append( self.vectorisationFn(  d ) )
            dst.pop(0) # means that vectorisation is done 

        t = Thread(target=do, args=( ) )
        assert len(dst) == 0
        dst.append( t ) # fisrst element the thread means that its doing
        t.setDaemon(True )
        t.start()


    # this generator yields a single vectorized data point at a time
    def dataPointVecGenerator(self):
        cacheBuffer = []
        dataEntriesBatchGen = self.getDataEntriesBatch( self.batchSize )

        for i in range( self.nJobs ):
            cacheBuffer.append([])
            self.vectorizeInBG( dataEntriesBatchGen.next() , cacheBuffer[-1] )

        while True:
            assert len(cacheBuffer) > 0
            assert len(cacheBuffer[0]) > 0
            if type(cacheBuffer[0][0]) is Thread:

                try:
                    cacheBuffer[0][0].join() # wait for the job if it is vectorizing
                except Exception, e:
                    print e

            for vecPoint in cacheBuffer[0]:
                yield vecPoint

            cacheBuffer.pop(0)
            cacheBuffer.append([])
            self.vectorizeInBG( dataEntriesBatchGen.next() , cacheBuffer[-1] )


    # this one  is a single point geenartor to batch generator converter
    def batchGenerator(self):
        return batchifyGenerator( self.dataPointVecGenerator() , self.batchSize  )

