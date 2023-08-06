from keras.backend.tensorflow_backend import set_session
import tensorflow as tf

def allow_growth():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth=True
    set_session(tf.Session(config=config))
    
    
def showKerasModel(m):
    from IPython.display import SVG
    from keras.utils.vis_utils import model_to_dot
    return SVG(model_to_dot( m  , show_shapes=True).create(prog='dot', format='svg'))


def set_gpu( gpu_id ):
    import os
    os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)

    
from tqdm import tqdm

from tqdm import tqdm

# returns ground tructh array and corresponding predicted array
def predict_generator_and_gt( model , generator , steps = None  , verbose=False ):

    # vectorizer.reset()
    # predictions = model.predict_generator( vectorizer.generator() ,  vectorizer.totalDataPoints )

    Y = None
    YP = None
    n = 0
    itt = generator
    if verbose:
        if not steps is None:
            itt = tqdm(itt , total=steps)
        else:
            itt = tqdm(itt )
    
    for x , y  in  itt  :

        yp = model.predict_on_batch( x )

        if Y is None:
            Y = y
        else:
            Y = np.concatenate( ( Y , y ))

        if YP is None:
            YP = yp
        else:
            YP = np.concatenate( ( YP , yp ))
            
        n += 1
        if ( not steps is None ) and n >= steps:
            break

    return Y , YP

    
    

import matplotlib as mpl
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



import pickle
from keras.callbacks import Callback


import pickle
from keras.callbacks import Callback


class WeightsPredictionsSaver(Callback):
    def __init__(self , saveName , val_data , saveFreq=1 , save_model=True , save_weights=True ,  save_preds = True ):

        self.saveName = saveName
        self.saveFreq = saveFreq
        self.epoch = 0
        self.val_data = val_data
        self.preds = { "GT":None , "X":None , "PR" : []  }
        self.save_model = save_model
        self.save_weights = save_weights
        self.save_preds = save_preds

    def on_epoch_end(self, batch, logs={}):
        if self.epoch % self.saveFreq == 0:
            
            if self.save_weights:
                self.model.save_weights( self.saveName + ".%d"%(self.epoch ) )
            
            if self.save_model:
                self.model.save( self.saveName + ".%d.model"%(self.epoch ) )
            
            
            if self.save_preds:
                self.preds['GT'] = self.val_data[1]
                self.preds['X'] = self.val_data[0]
                pr = self.model.predict( self.val_data[0]  )
                self.preds['PR'].append( pr  )
                pickle.dump( self.preds , open( self.saveName +".preds.pkl" ,"wb"))
        self.epoch += 1

