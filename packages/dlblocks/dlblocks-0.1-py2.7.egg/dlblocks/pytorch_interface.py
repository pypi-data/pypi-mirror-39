
# coding: utf-8

# In[6]:


import torch.utils.data
from torch import optim
import torch.backends.cudnn as cudnn
from torchvision import datasets, transforms
from torchvision.utils import save_image
from torch.autograd import Variable , Function
from torch import nn
from torch.nn import functional as F
import torch


from collections import defaultdict
from tqdm import tqdm


# In[3]:


import numpy as np


# In[1]:


from types import MethodType


# In[5]:


def make_var( data , cuda=True ):
    if type( data ) is tuple:
        return tuple([ make_var(d) for d in data  ])
    elif type( data ) is list:
        return list([ make_var(d) for d in data  ])
    else:
        r =  Variable( torch.from_numpy(data) )
        if cuda:
            r = r.cuda()
        return r



# In[9]:




def pytorch_train_on_batch( model , x , y , optimizer=None ):

    """
    the forward function should take the list on inputs/ or input and return a list of outputs / or output
    the loss function should take x , y , and model output ... it should return loss Variale and ( optional) a ditionary of seperate losses 
    """

    x = make_var( x )

    if not y is None:
        y = make_var( y )

    if optimizer is None:
        optimizer = model.optimizer 

    optimizer.zero_grad()
    outputs = model(x)

    loss = model.loss_function(x,y,outputs )
    latest_losses = {}
    if type(loss) is tuple:
        loss , latest_losses = loss
    loss.backward()
    optimizer.step()

    losses = {}
    losses['loss'] = loss.cpu().data.numpy()

    for key in latest_losses:
        losses[key + '_train'] = ( latest_losses[key].cpu().data.numpy() )

    return losses






# In[8]:



def pytorch_fit_generator(model , generator, steps_per_epoch, epochs=1, verbose=1, optimizer=None ,epoch_callback=None ):

    """
    This assumes that there is a loss_fucntion attached to the model class. 
    The generatr should yield x,y or just x
    """

    if optimizer is None:
        optimizer = model.optimizer 

    for ep in range( epochs ): 

        model.train()

        losses = defaultdict( list )
        if verbose:
            bar = tqdm(range(steps_per_epoch))
        else:
            bar = (range(steps_per_epoch))

        for batch_idx  in bar :
            data = generator.next()
            if  type( data ) is tuple :
                x , y  = data
            else:
                x = data
                y = None

            latest_losses = pytorch_train_on_batch( model , x , y , optimizer=optimizer )

            for key in latest_losses:
                losses[key ].append( latest_losses[key] )

            if verbose:
                loss_string = ' '.join(['{}: {:.6f}'.format(k, np.mean(v)  ) for k, v in losses.items()])
                bar.set_description( loss_string )

                
                
def get_steps_per_epoch(x , y ,batch_size):
    if type(x) is list:
        n_elements = x[0].shape[0]
    else:
        n_elements = x.shape[0]
    return int( n_elements*1.0/batch_size )


def make_generator( x , y , batch_size ):
    steps_per_epoch = get_steps_per_epoch(x , y ,batch_size)
    while True:
        for b_i in range( steps_per_epoch ):
            if type( x ) is list:
                x_yield = [  np.array(xx[b_i*batch_size : (b_i+1)*batch_size ]) for xx in x  ]
            else:
                x_yield = np.array(x[b_i*batch_size : (b_i+1)*batch_size ] )
                
            if y is None:
                y_yield  = None
            elif type( y ) is list:
                y_yield = [  np.array(yy[b_i*batch_size : (b_i+1)*batch_size ] )for yy in y  ]
            else:
                y_yield = np.array(y[b_i*batch_size : (b_i+1)*batch_size ] )
                
            yield x_yield , y_yield

            

def pytorch_fit( model , x=None, y=None, batch_size=32, epochs=1, verbose=1,optimizer=None ,epoch_callback=None ):
    steps_per_epoch = get_steps_per_epoch( x , y ,batch_size=batch_size )
    g = make_generator( x , y ,  batch_size=batch_size)
    
    pytorch_fit_generator(model , g, steps_per_epoch, epochs=epochs, verbose=verbose, optimizer=optimizer ,epoch_callback=epoch_callback )


# In[14]:


def get_loss_fn_from_str( loss_name ):
    
    loss_fn_dict = { 
        'mse': F.mse_loss , 
        'mean_squared_error': F.mse_loss , 
        'bce': F.binary_cross_entropy ,
        'binary_cross_entropy' : F.binary_cross_entropy , 
        'smooth_l1_loss' : F.smooth_l1_loss , 
        'cross_entropy' : F.cross_entropy
    }
    
    pt_loss_fn = loss_fn_dict[ loss_name ]
    
    def loss_function(self, x=None , y=None , model_output=None ):
        return pt_loss_fn(  model_output , y )
    
    return loss_function


# In[15]:


def aggregate_loss_list( losses , loss_weights=None ):
    assert type(losses) is list
    new_losses = []
    for loss in losses:
        if type( loss ) is str or type( loss ) is unicode:
            new_losses.append( get_loss_fn_from_str(loss) )
        else:
            new_losses.append( loss )
    losses = new_losses
    loss_weights2 = loss_weights
    
    def loss_function(self, x=None , y=None , model_output=None ):
        if y is None:
            y = [None ]*len(model_output)
            
        if loss_weights2 is None:
            loss_weights2 = [ 1.0 ]*len(model_output)
            
        loss_t = None
        
        for i , (yp , op , lw) in enumerate( zip( y , model_output , loss_weights ) ) :
            loss_tt = lw*losses[i]( x , yp , op )
            if i == 0:
                loss_t = loss_tt
            else:
                loss_t += loss_tt
        
        return loss_t
    
    return loss_function
            
    
    


# In[16]:


def pytorch_compile( model , optimizer=None , loss=None ):
    
    opts_dict = { 'sgd':optim.SGD , 'adam' :optim.Adam , 'adadelta': optim.Adadelta , 'adagrad': optim.Adagrad , 'rmsprop':optim.RMSprop }    
    
    if not optimizer is None:
        if type(optimizer) is str or type(optimizer) is unicode:
            optimizer = opts_dict[optimizer](model.parameters() )
        model.optimizer = optimizer
    
    if not loss is None:
        if type( loss ) is list:
            loss = aggregate_loss_list( loss )
        elif type( loss ) is str or type( loss ) is unicode:
            loss = ( get_loss_fn_from_str(loss) )
            
        model.loss_function = MethodType( loss, model )
        
    
        


# In[19]:

def split_batches( x ,  batch_size ):
    steps_per_epoch = get_steps_per_epoch(x , x ,batch_size )+1
    for b_i in range( steps_per_epoch ):
        if type( x ) is list:
            x_yield = [  np.array(xx[b_i*batch_size : (b_i+1)*batch_size ]) for xx in x  ]
            if x_yield[0].shape[0] == 0:
                return
        else:
            x_yield = np.array(x[b_i*batch_size : (b_i+1)*batch_size ] )
            if x_yield.shape[0] == 0:
                return

        yield x_yield




def pytorch_predict_batch( model , x ):
    x = make_var( x )
    out = model(x)
    if type( out ) is list:
        out = [  o.cpu().data.numpy()  for o in out ]
    else:
        out = out.cpu().data.numpy()
    return out



def pytorch_predict( model , x , batch_size=16):
    x_list = list(split_batches(x ,batch_size ))
    return np.concatenate([pytorch_predict_batch( model , x ) for x in x_list])




# In[ ]:


def pytorch_save_weights( model , weights_path ):
    torch.save(model.state_dict(), weights_path)
    
def pytorch_load_weights( model , weights_path ):
    model.load_state_dict(torch.load(weights_path))


# In[17]:



def attach_interface_functions( model ):
    model.fit_generator = MethodType( pytorch_fit_generator , model )
    model.fit = MethodType( pytorch_fit , model )
    model.compile = MethodType( pytorch_compile , model )
    model.train_on_batch = MethodType( pytorch_train_on_batch , model )
    model.predict = MethodType( pytorch_predict , model )
    model.predict_on_batch = MethodType( pytorch_predict_batch , model )
    model.save_weights = MethodType( pytorch_save_weights , model )
    model.load_weights = MethodType( pytorch_load_weights , model )
    

### Nice utils : https://github.com/davidcpage/cifar10-fast/blob/master/utils.py
    
class Flatten(nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return x
    
    
class Reshape(nn.Module):
    def __init__(self , shape ):
        self.shape = shape 
        super(Reshape, self).__init__()

    def forward(self, x):
        x = x.view(*((x.size(0),)+ self.shape)  )
        return x
    
    
class Identity(nn.Module):
    def forward(self, x): return x
    
    
class Mul(nn.Module):
    def __init__(self, weight):
        super().__init__()
        self.weight = weight
    def __call__(self, x): 
        return x*self.weight
    
    
class Add(nn.Module):
    def forward(self, x, y): return x + y 
    
def to_numpy(x):
    return x.detach().cpu().numpy()  


