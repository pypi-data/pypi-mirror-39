import chainer
import chainer.functions as F
import chainer.links as L

from chainer_addons.models import PretrainedModelMixin

from os.path import isfile
from skimage.transform import resize

from .blocks import Inception1
from .blocks import Inception2
from .blocks import Inception3
from .blocks import Inception4
from .blocks import Inception5
from .blocks import InceptionHead
from .link_mappings import chainer_to_keras

import numpy as np

def __pooling_op(operation):
	if operation == "avg":
		return F.average_pooling_2d
	elif operation == "max":
		return F.max_pooling_2d
	else:
		raise ValueError("Unkown pooling operation: {}".format(operation))

def global_pooling(operation):
	def inner(x):
		ksize = x.shape[2:]
		return __pooling_op(operation)(x, ksize)
	return inner

def pooling(operation, ksize, stride=1, pad=0):
	def inner(x):
		return __pooling_op(operation)(x, ksize, stride, pad)
	return inner

class InceptionV3(chainer.Chain, PretrainedModelMixin):

	class meta:
		input_size = 299
		n_conv_maps = 2048
		feature_size = 2048
		mean = np.array([127.5, 127.5, 127.5], dtype=np.float32).reshape(3,1,1)
		# prepare_func = prepare

		classifier_layers = ["fc"]
		conv_map_layer = "body"
		feature_layer = "pool"

		@staticmethod
		def prepare_func(x, size):
			x = resize(x, size, mode="constant")
			x = x.transpose(2,0,1)
			# rescale to [-1..1]
			x = x.astype(np.float32) * 2 - 1
			# swap channels
			x = x[:, :, ::-1]
			return x

	def __init__(self, pretrained_model, n_classes):
		super(InceptionV3, self).__init__()

		with self.init_scope():
			self.head = InceptionHead()

			pool_args = dict(operation="avg", ksize=3, stride=1, pad=1)
			self.mixed00 = Inception1(insize=192, sizes=[48, 64, 96], outputs=[64, 64, 96, 32], **pool_args)
			self.mixed01 = Inception1(insize=256, sizes=[48, 64, 96], outputs=[64, 64, 96, 64], **pool_args)
			self.mixed02 = Inception1(insize=288, sizes=[48, 64, 96], outputs=[64, 64, 96, 64], **pool_args)

			pool_args = dict(operation="max", ksize=3, stride=2, pad=0)
			self.mixed03 = Inception2(288, sizes=[64, 96], outputs=[384, 96], **pool_args)

			pool_args = dict(operation="avg", ksize=3, stride=1, pad=1)
			self.mixed04 = Inception3(768, sizes=[128] * 6, outputs=[192] * 4, **pool_args)
			self.mixed05 = Inception3(768, sizes=[160] * 6, outputs=[192] * 4, **pool_args)
			self.mixed06 = Inception3(768, sizes=[160] * 6, outputs=[192] * 4, **pool_args)
			self.mixed07 = Inception3(768, sizes=[192] * 6, outputs=[192] * 4, **pool_args)

			pool_args = dict(operation="max", ksize=3, stride=2, pad=0)
			self.mixed08 = Inception4(768, sizes=[192] * 4, outputs=[320, 192], **pool_args)

			# here the middle outputs are doubled!
			pool_args = dict(operation="avg", ksize=3, stride=1, pad=1)
			self.mixed09 = Inception5(1280, sizes=[384, 448, 384], outputs=[320, 384, 384, 192], **pool_args)
			self.mixed10 = Inception5(2048, sizes=[384, 448, 384], outputs=[320, 384, 384, 192], **pool_args)

			self.pool = global_pooling("avg")
			self.fc = L.Linear(2048, n_classes)

		if pretrained_model is not None and isfile(pretrained_model):
			if pretrained_model.endswith(".h5"):
				self._load_from_keras(pretrained_model)
			else:
				from chainer.serializers import load_npz
				load_npz(pretrained_model, self)

	@property
	def _links(self):
		return [
			("head", [self.head]),
			("body", [getattr(self, "mixed{:02d}".format(i)) for i in range(11)]),
			("pool", [self.pool]),
			("fc", [self.fc]),
		]

	def extract(self, x):
		x = self.head(x)
		x = self.mixed00(x)
		x = self.mixed01(x)
		x = self.mixed02(x)
		x = self.mixed03(x)
		x = self.mixed04(x)
		x = self.mixed05(x)
		x = self.mixed06(x)
		x = self.mixed07(x)
		x = self.mixed08(x)
		x = self.mixed09(x)
		x = self.mixed10(x)

		return self.pool(x)


	def __call__(self, x, layer_name='fc'):
		h = x
		for key, funcs in self.functions.items():
			for func in funcs:
				h = func(h)
			if key == layer_name:
				return h

	def _load_from_keras(self, weights):
		import h5py
		def _assign(name, param, data):
			assert data.shape == param.shape, \
				"\"{}\" does not match the shape: {} != {}!".format(
					name, data.shape, param.shape)
			if isinstance(param, chainer.variable.Parameter):
				param.data[:] = data
			else:
				param[:] = data


		with h5py.File(weights, "r") as f:
			for name, link in self.namedlinks(skipself=True):
				if name not in chainer_to_keras: continue
				keras_key = chainer_to_keras[name]

				if isinstance(link, L.Convolution2D):
					W = np.asarray(f[keras_key][keras_key + "/kernel:0"])
					W = W.transpose(3,2,0,1)

					_assign(name, link.W, W)

				elif isinstance(link, L.Linear):
					W = np.asarray(f[keras_key][keras_key + "/kernel:0"])
					b = np.asarray(f[keras_key][keras_key + "/bias:0"])

					_assign(name, link.W, W.transpose(1,0))
					_assign(name, link.b, b)

				elif isinstance(link, L.BatchNormalization):
					beta = np.asarray(f[keras_key][keras_key + "/beta:0"])
					avg_mean = np.asarray(f[keras_key][keras_key + "/moving_mean:0"])
					avg_var = np.asarray(f[keras_key][keras_key + "/moving_variance:0"])

					_assign(name, link.beta, beta)
					_assign(name, link.avg_mean, avg_mean)
					_assign(name, link.avg_var, avg_var)

				else:
					raise ValueError("Unkown link type: {}!".format(type(link)))


# if __name__ == '__main__':
# 	import sys
# 	pretrained_model = None

# 	if len(sys.argv) >= 2:
# 		pretrained_model = sys.argv[1]

# 	model = InceptionV3(pretrained_model, n_classes=1000)

# 	model.to_gpu(0)
# 	var = model.xp.array(np.random.randn(8, 3, 299, 299).astype(np.float32))

# 	with chainer.using_config("train", False):
# 		pred = model(var)
# 	# import pdb; pdb.set_trace()


