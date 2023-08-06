
from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
from torch.autograd import Variable




from collections import defaultdict
from tqdm import tqdm

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


    
def pytorch_fit_generator(epochs , model, generator , steps_per_epoch , optimizer=None , epoch_callback=None , cuda=True  ):
    
    """
    This assumes that there is a loss_fucntion attached to the model class. 
    The loss function is provided with the generator output and the model output concateneted
    """
    
    if optimizer is None:
        optimizer = model.optimizer 
        
    for ep in range( epochs ): 
    
        model.train()

        losses = defaultdict( list )
        bar = tqdm(range(steps_per_epoch))
        for batch_idx  in bar :
            data   = generator.next()
            if not type( data ) is tuple :
                data = (data,)
            data = make_var(data)
            optimizer.zero_grad()
            
            outputs = model(*data)
            
            if not type( outputs ) is tuple :
                outputs = (outputs,)
            
            
            loss , latest_losses = model.loss_function( *(data + outputs) )
            loss.backward()
            optimizer.step()


            for key in latest_losses:
                losses[key + '_train'].append( latest_losses[key].cpu().data.numpy() )

            loss_string = ' '.join(['{}: {:.6f}'.format(k, np.mean(v)  ) for k, v in losses.items()])
            bar.set_description( loss_string )

        if not epoch_callback is None:
            epoch_callback( data , outputs  )
    
    
    
    
    
# numpy array to pytorch varalble of that type
def ptVarType( a ):
	if a.dtype == 'int64':
		return torch.LongTensor
	if 'float' in str( a.dtype ):
		return torch.FloatTensor


def addDict( a , b ):
	if a is None:
		return b
	if b is None :
		return a

	c = {}
	for k in a.keys():
		c[k] = a[k] + b[k]

	return c

def fit_generator_pt_2( model , optim , criterion , generator , steps_per_epoch ,  epochs=1 ):

	x_np , y_np = generator.next()

	x = Variable( ptVarType(x_np)( *(x_np.shape) )).cuda()
	y = Variable( ptVarType(y_np)( *(y_np.shape)  )).cuda()

	for ep in range( epochs ):

		loss_vals = []
		bar = tqdm( range(steps_per_epoch))
		for i in bar :

			x_np , y_np = generator.next()

			x.data.copy_( torch.from_numpy( x_np ) )
			y.data.copy_( torch.from_numpy( y_np ) )

			optim.zero_grad()
			y_pred = model( x )

			loss = criterion( y_pred , y  )
			loss.backward()
			optim.step()

			loss_val = loss.data[0] 
			loss_vals.append( loss_val )
			bar.set_description('loss : %f' % np.mean(loss_vals) )


def evaluate_generator_pt( model , eval_fn , generator , steps , verbose=False ):
	ev = None
	n = 0

	x_np , y_np = generator.next()

	x = Variable( ptVarType(x_np)( *(x_np.shape) )).cuda()
	y = Variable( ptVarType(y_np)( *(y_np.shape)  )).cuda()

	if verbose:
		bar = tqdm( range(steps))
	else:
		bar = range(steps)

	for i in bar:
		
		x.data.copy_( torch.from_numpy( x_np ) )
		y.data.copy_( torch.from_numpy( y_np ) )

		y_pred_np = model( x ).cpu().data.numpy()
		ev = addDict( ev , eval_fn( y_np ,  y_pred_np )  )
		n += 1

		if i == steps-1:
			break

		x_np , y_np = generator.next()

	for k in ev.keys():
		ev[ k ] = ev[ k ]/(n+ 0.0 )

	return ev

