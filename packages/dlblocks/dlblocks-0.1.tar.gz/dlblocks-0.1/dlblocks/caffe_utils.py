
from caffe.proto import caffe_pb2
import google.protobuf.text_format as txtf




def netFromProto( fn ):
	net = caffe_pb2.NetParameter()
	with open(fn) as f:
		s = f.read()
		txtf.Merge(s, net)
	return net

def netFromString( s ):
	net = caffe_pb2.NetParameter()
	txtf.Merge(s, net)
	return net



def layerFromName( net , layerName ):
	layerNames = [l.name for l in net.layer]
	idx = layerNames.index( layerName )
	return net.layer[idx]



def layersToProto( layers ):
	return "\n".join([ "layer {\n " + str( l ) + "\n } " for l in layers  ])


def netToProto(net ):
	if hasattr( net   , "__getitem__") :
		return layersToProto( net  )
	else:
		return str( net )

def mapLayersName( layers , map_fnn ,  filter_fn = None ):
		
	if type(map_fnn) is unicode or  type(map_fnn) is str :
		map_fn =  lambda p : ( p + ""  + map_fnn )
	else:
		map_fn = map_fnn
	
	allNames = [ l.name for l in layers  ]
	for l in layers:
		if type( l.top )  in [ unicode , str ]:
			allNames.append( l.top )
		elif type( l.top[:] )  in [ list ]:
			allNames += l.top[:]

	mapping  = [ ( l.name, map_fn( l.name )) for l in layers if ( filter_fn  is None or filter_fn(l.name) )  ]
	mapping  = dict( mapping  )
	
	for l in layers:
		if  l.name in mapping :
			l.name = mapping[ l.name ]
			
		if type( l.top )  in [ unicode , str ] and l.top in mapping :
			l.top = mapping[ l.top ]
		elif hasattr( l.top   , "__getitem__")  :
			for i in range( len( l.top ) ) :
				if l.top[i] in mapping:
					l.top[i] = mapping[  l.top[i]  ]
					
		if type( l.bottom )  in [ unicode , str ] and l.bottom in mapping :
			l.bottom = mapping[ l.bottom ]
		elif hasattr( l.top   , "__getitem__")  :
			for i in range( len( l.bottom ) ) :
				if l.bottom[i] in mapping:
					l.bottom[i] = mapping[  l.bottom[i]  ]
	
			
			
def clone( net ):

	net_str = netToProto( net )
	new_net = caffe_pb2.NetParameter()
	txtf.Merge( net_str  , new_net)

	return  new_net
	
	
def mapParamsName( layers , map_fnn ,  filter_fn = None ):
	
	if type(map_fnn) is unicode or  type(map_fnn) is str :
		map_fn =  lambda p : ( p + ""  + map_fnn )
	else:
		map_fn = map_fnn
		
		
	for i in range( len( layers )):
		for j in range(len(layers[i].param)):
			if layers[i].param[j].name != '' and ( filter_fn is None or  filter_fn(layers[i].param[j].name) ) :
				layers[i].param[j].name  = map_fn( layers[i].param[j].name  )
			
	
	
	

def addParamNames( layers ):
	for i in range( len( layers )):
		for j in range(len(layers[i].param)):
			if layers[i].param[j].name == '':
				layers[i].param[j].name  = layers[i].name + "_" + str(j)
		 



# map_fnn[ source ] -> target
def transferWeights(  source_prototxt , source_weights , target_prototxt , target_weights_load , target_weights_save  , map_fnn ):
	
	import caffe

	if type(map_fnn) is unicode or  type(map_fnn) is str :
		map_fn =  lambda p : ( p + ""  + map_fnn )
	else:
		map_fn = map_fnn


	src_net = caffe.Net( source_prototxt, source_weights , caffe.TRAIN)

	if target_weights_load  is None:
		tgt_net = caffe.Net(target_prototxt, caffe.TRAIN )
	else:
		tgt_net = caffe.Net(target_prototxt, target_weights_load  , caffe.TRAIN )
	
	src_names = src_net.params.keys()
	tgt_names = tgt_net.params.keys()

	for src_name in src_names:
		tgt_name = map_fn(  src_name )
		if tgt_name in tgt_names:
			print "copied " , src_name , " -> " , tgt_name
			for p, q in zip(tgt_net.params[tgt_name], src_net.params[src_name]):
				p.data[...] = q.data
		else:
			print "ignoring " , tgt_name

	tgt_net.save( target_weights_save  )



# map_fnn[ source ] -> target
def transferWeights(  source_prototxt , source_weights , target_prototxt , target_weights_load , target_weights_save  , map_fnn ):
	
	import caffe

	if type(map_fnn) is unicode or  type(map_fnn) is str :
		map_fn =  lambda p : ( p + ""  + map_fnn )
	else:
		map_fn = map_fnn


	src_net = caffe.Net( source_prototxt, source_weights , caffe.TRAIN)

	if target_weights_load  is None:
		tgt_net = caffe.Net(target_prototxt, caffe.TRAIN )
	else:
		tgt_net = caffe.Net(target_prototxt, target_weights_load  , caffe.TRAIN )
	
	src_names = src_net.params.keys()
	tgt_names = tgt_net.params.keys()

	for src_name in src_names:
		tgt_name = map_fn(  src_name )
		if tgt_name in tgt_names:
			print "copied " , src_name , " -> " , tgt_name
			for p, q in zip(tgt_net.params[tgt_name], src_net.params[src_name]):
				p.data[...] = q.data
		else:
			print "ignoring " , tgt_name

	tgt_net.save( target_weights_save  )



def classificationFCLayer( layer_name ,  num_out , layer_bottom , layer_bottom_label , loss_weight=1   ):

	return """

	layer {
	  name: "%s"
	  type: "InnerProduct"
	  bottom: "%s"
	  top: "%s"
	  param {
	    lr_mult: 1
	    decay_mult: 1
	  }
	  inner_product_param {
	    num_output: %d
	  }
	}

	layer {
	  name: "%s_loss"
	  type: "SoftmaxWithLoss"
	  bottom: "%s"
	  bottom: "%s"
	  top: "%s_loss"
	  loss_weight : %f
	}

	layer {
	  name: "%s_accuracy"
	  type: "Accuracy"
	  bottom: "%s"
	  bottom: "%s"
	  top: "%s_accuracy"
	  include {
	    phase: TEST
	  }
	}

	""" % (  layer_name , layer_bottom , layer_name , num_out , layer_name , layer_name ,layer_bottom_label ,layer_name , loss_weight , layer_name , layer_name , layer_bottom_label , layer_name  )




def classificationFCLayerDeploy( layer_name ,  num_out , layer_bottom   ):

	return """

	layer {
	  name: "%s"
	  type: "InnerProduct"
	  bottom: "%s"
	  top: "%s"
	  param {
	    lr_mult: 1
	    decay_mult: 1
	  }
	  inner_product_param {
	    num_output: %d
	  }
	}

	layer {
	  name: "prob"
	  type: "Softmax"
	  bottom: "%s"
	  top: "prob"
	}


	""" % (  layer_name , layer_bottom , layer_name , num_out , layer_name  )

 
# net = netFromProto( 'train_new.prototxt' )
# addParamNames( net.layer )
# net = clone( net.layer[ : -2 ] )
# net2 = clone( net.layer[-10 :]  )
# mapParamsName( net2.layer , "b2"  )
# mapLayersName( net2.layer , "b2")
# net2.layer[0].bottom[0] =  net.layer[-10].bottom[0]

# print str( net ) + "\n" + str( net2)
	
	