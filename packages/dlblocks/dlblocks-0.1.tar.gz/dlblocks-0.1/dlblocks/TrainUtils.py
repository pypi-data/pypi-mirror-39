
import math
from threading import Thread
import json

import numpy as np
from functools import partial


import random
import json
import os
import numpy as np



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

		self.defaultGen = self.generator()

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
	def generator(self):
		return batchifyGenerator( self.dataPointVecGenerator() , self.batchSize  )
		

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

		if type (d) is dict :

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

			x , y  = d

			if type(x) is list or  type(x) is tuple:
				isFusionModelVec = True
				fusionModelVecL = len( x )
				if fusionXs is None:
					fusionXs = [   []  for _ in range(fusionModelVecL)  ]

				for i in range( fusionModelVecL ):
					fusionXs[i].append( x[i] )

			else:
				X.append(x)
			
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
				
				if not isFusionModelVecY:
					yieldY = np.array(Y)
					Y = []
				else:
					yieldY =  [ np.array(fusionYs[i]) for i in range(fusionModelVecLY)  ] 
					fusionYs = [   []  for _ in range(fusionModelVecLY)  ]

				nDone = 0
				yield yieldX , yieldY
				



def trainModel( model , train_vectorizer , nEpochs , val_vectoriser = None , minibatchsize = 30 ):

	while True:
		vec = train_vectorizer.getNext()
		cur_epoch =  train_vectorizer.totalBatchesDone% train_vectorizer.totalBatches
		cur_batch = train_vectorizer.batchesDone

		if cur_epoch >= nEpochs:
			break

		print "Epoch " , cur_epoch , "Batch " , cur_batch
		if val_vectoriser is None:
			loss =  model.fit( *vec ,  batch_size=minibatchsize , nb_epoch=1 ).history['loss'][-1]
			print "Loss -> " , loss
		else :
			loss =  model.fit( *vec ,  batch_size=minibatchsize , nb_epoch=1 , validation_data= val_vectoriser.getNext()   ).history['loss'][-1]
			print "Loss -> " , loss
		



def trainModel2( model ,  train_vectorizer , nBatchIter ):
	
	import progressbar
	bar = progressbar.ProgressBar()

	losses = []

	for i in bar(range(nBatchIter)):
		vec = train_vectorizer.getNext()
		loss = model.train_on_batch( *vec  )

		losses.append( loss )

	print "Loss -> " , np.mean( losses  , axis=1)


def theList( l ):
	return [ float( a ) for a in list(l) ]




# modelsNVectorizers -> [ ( modelName , model , vectorizer , n ) ]   # n = weight of that model
# validationModelsNVectorizers ->  [ ( modelName , model , vectorizer , nValbatches ) ]
def jointlyTrainModel( modelsNVectorizers ,  nEpochs , nBatchIter , validationModelsNVectorizers=[]  ):

	losses = {}
	trainlossesMean = {}
	valLossesMean = {}

	for j in range(nEpochs):
		import progressbar
		bar = progressbar.ProgressBar()

		for ( modelName , model , vectorizer , n ) in modelsNVectorizers:
			losses[ modelName ] = []

		for i in bar(range(nBatchIter)):
			for ( modelName , model , vectorizer , n ) in modelsNVectorizers:

				for k in range( n ):
					vec = vectorizer.getNext()
					loss = model.train_on_batch( *vec  )
					losses[modelName].append( loss   )

		print "==================="	
		print "Epoch " , j 

		for ( modelName , model , vectorizer , n ) in modelsNVectorizers:
			print modelName , " -> " , np.mean( losses[modelName] ,  axis=0 )
			trainlossesMean[modelName] = theList(  np.mean( losses[modelName] ,  axis=0 ) )

		if len(validationModelsNVectorizers) > 0 :
			print "------------"
			print "Validation results :  "
			for ( modelName , model , vectorizer , nValbatches )  in validationModelsNVectorizers :
				val_losses = []
				for i in range( nValbatches ) :
					vec = vectorizer.getNext()
					val_losses.append( model.test_on_batch( *vec  ) )
				print modelName , " -> " , np.mean( val_losses ,  axis=0 )
				valLossesMean[modelName] = theList( np.mean( val_losses ,  axis=0 )  )

		print "==================="

	return trainlossesMean , valLossesMean











# returns ground tructh array and corresponding predicted array
def getGroundTruthNPredictions( model , vectorizer  ):

	# vectorizer.reset()
	# predictions = model.predict_generator( vectorizer.generator() ,  vectorizer.totalDataPoints )

	Y = None
	YP = None

	vectorizer.reset()
	for i in range( vectorizer.totalBatches ):

		x , y  = vectorizer.getNext()
		yp = model.predict_on_batch( x )

		if Y is None:
			Y = y
		else:
			Y = np.concatenate( ( Y , y ))

		if YP is None:
			YP = yp
		else:
			YP = np.concatenate( ( YP , yp ))

	return Y , YP








class BaseTrainer():

    def __init__(self, exp_location="./" , exp_name=None , config_file=None, config_args={} ):

        self.built = False
        self.dataset_set = False
        self.exp_location = exp_location

        if not config_file is None:
            config = json.loads( open(config_file).read())
        else:
            config = {}

        for k in config_args:
            config[k] = config_args[k]
            
            
        if exp_name is None:
            if "exp_name" in config:
                exp_name = config['exp_name']
            else:
                exp_name = str( random.randint(0 , 99999 ))

        self.exp_name = exp_name
        self.config = config
        open( os.path.join( self.exp_location  , self.exp_name+".config.json" ) , "w" ).write( json.dumps( self.config ) )
        self.n_epochs = config['epochs']

        from numpy.random import seed
        seed(966)
        from tensorflow import set_random_seed
        set_random_seed(988)

        

    def build_model(self):
        self.built = True
        # plot_model( self.model, to_file=os.path.join(  self.exp_location , self.exp_name +"_model.png" )    )

    def set_dataset(self):
        self.dataset_set = True


    def train( self ):
        
        

        if not self.built:
            self.build_model()

        if not self.dataset_set:
            self.set_dataset()
            
        from keras_utils import WeightsPredictionsSaver
        self.svr = WeightsPredictionsSaver( os.path.join(  self.exp_location , self.exp_name  )   , ( self.te_data_inp  , self.te_data_data_target ) , save_model=False , save_weights=False  )


        self.model.fit( self.data_inp , self.data_target , epochs=self.n_epochs ,callbacks=[self.svr]  )

        self.evaluate()

    def evaluate( self ):
        pass





from threading import Thread
from functools import partial


def parallizeGenerator( gen ):
	#
	queue = []
	stopped = [False]
	#
	def worker():
		for X in gen:
			while( len(queue)) > 10:
				pass
			queue.append( X )
		# print "K"
		stopped[0] = True
	#
	from threading import Thread
	t = Thread(target=worker, args=() )
	t.setDaemon(True )
	t.start()
	#
	while True:
		if stopped[0]:
			# print "hoho"
			break


		while len(queue) == 0:
			pass
		yield queue.pop(0)





def equalSample( data , attribute ):
	classes = {}
	for d in data:
		classes[ d[attribute] ] = True
	classes = list( classes.keys()  )

	queues = {}
	for classs in classes:
		queues[classs] = []

	for d in data:
		queues[  d[attribute]  ].append( d )

	while True:
		for classs in classes:
			d = queues[  classs  ].pop(0)
			queues[  classs  ].append( d )
			yield d

	


def evalueteEnsemble( models , gen , n_samples ):
	# "THIS IS WRONG AS JUST AVERAGING THE RESULTS :/"
	nDone = 0	
	nAvg = 0
	accVec = None
	while nDone < n_samples:
		x , y  = gen.next()
		if type(x ) is list:
			batchSize = x[0].shape[0]
		else:	
			batchSize = x.shape[0]
		nDone += batchSize
		for model in models:
			t = model.test_on_batch( x , y )
			print model.metrics_names
			print "t.sh -> " , len(t)
			t = np.array(t)

			if accVec is None:
				accVec = t
			else:
				accVec = accVec + t
			nAvg += 1
	print accVec/nAvg
	return accVec/nAvg







import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from keras.callbacks import  Callback

class PlotEpochs( Callback):
    
    def __init__(self , filename , title=''):
        self.filename = filename
        self.title = title
        super(PlotEpochs, self).__init__()
    
    def on_train_begin(self, logs={}):
        self.losses = {}
        self.accuracies = {}
        

    def on_epoch_end(self, batch, logs={}):
#         self.losses.append(logs.get('loss'))
#         print logs
#         print "lll", logs.get('loss')


        for key in logs.keys():
            if "loss" in key and  not key in self.losses:
                self.losses[key] = []
            if "acc" in key and  not key in self.accuracies:
                self.accuracies[key] = []
            
            if "loss" in key:
                self.losses[key].append( logs[key] )
            if "acc" in key:
                self.accuracies[key].append( logs[key] )
                
        self.plot()
                
    def on_train_end( self , jjjj  ):
        self.plot()
        
        
    def plot(self ):
        # plot the accuracies
        scales = range( len( self.accuracies[ self.accuracies.keys()[0]  ]))
        fig = plt.figure()
        ax = fig.gca()
        ax.spines["top"].set_visible(False)  
        ax.spines["right"].set_visible(False)  
        
        for key in self.accuracies.keys():
            if "val" in key:
                plt.plot(scales, self.accuracies[key]  ,label=key )
            else:
                plt.plot(scales, self.accuracies[key] , '--'  ,label=key )

        plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on") 
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.title(self.title)
        plt.savefig(self.filename+'_acc.png' , bbox_inches='tight')
        
        plt.cla()
        
        fig = plt.figure()
        ax = fig.gca()
        ax.spines["top"].set_visible(False)  
        ax.spines["right"].set_visible(False)  
        
        for key in self.losses.keys():
            if "val" in key:
                plt.plot(scales, self.losses[key]  ,label=key )
            else:
                plt.plot(scales, self.losses[key] , '--'  ,label=key )


        plt.tick_params(axis="both", which="both", bottom="on", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on") 
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title(self.title)
        plt.savefig(self.filename+'_loss.png' , bbox_inches='tight')
        




def EpochLRChanger( initial_lrate=0.001 ,drop = 0.5, epochs_drop = 30.0 ):
	from keras.callbacks import LearningRateScheduler
	import math

	def step_decay(epoch):
		lrate = initial_lrate * math.pow(drop,  epoch/epochs_drop )
		return lrate

	return LearningRateScheduler(step_decay)




from keras.callbacks import Callback

class WeightsSaver(Callback):
    def __init__(self, model, saveName , saveFreq=1):
        self.model = model
        self.epoch = 0
        self.saveName = saveName
        self.saveFreq = saveFreq

    def on_epoch_end(self, batch, logs={}):
    	if self.epoch % self.saveFreq == 0:
	        self.model.save_weights( self.saveName + ".%d"%(self.epoch ) )
	        self.model.save( self.saveName + ".%d.model"%(self.epoch ) )
        self.epoch += 1

  


def infiniteGenerator( l ):
	while True:
		for item in l:
			yield item
        

       

            
