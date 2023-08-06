"""
here you can find some model definitions or modificated versions
of present models in chainer (eg. VGG19)
"""
import chainer
import chainer.functions as F
import chainer.links as L

from chainer.serializers import npz
from chainer_addons.links import PoolingType

from inspect import signature
from collections import OrderedDict
from chainer.initializers import HeNormal

import numpy as np

class Classifier(chainer.Chain):
	"""
		model wrapper, that is adapted for the DSL of
		the pretrained models in chainer_addons
	"""
	def __init__(self, model, layer_name=None):
		super(Classifier, self).__init__()
		with self.init_scope():
			self.model = model

		self.layer_name = layer_name

	def __call__(self, X, y):
		pred = self.model(X, layer_name=self.layer_name)
		loss, accu = F.softmax_cross_entropy(pred, y), F.accuracy(pred, y)

		chainer.report({
			"loss": loss.data,
			"accuracy": accu.data,
		}, self)
		return loss

class RNNClassifier(chainer.Chain):
	def __init__(self, model, layer_name=None, rnn_cls=L.LSTM, units=2048):
		super(RNNClassifier, self).__init__()
		with self.init_scope():
			self.model = model
			self.rnn = rnn_cls(model.meta.feature_size, units)
			self.clf = L.Linear(units, model.clf_layer.W.shape[0])

		self.layer_name = layer_name or model.meta.feature_layer

	def __call__(self, X, y):
		assert X.ndim == 5, "Incorrect input data format!"

		self.rnn.reset_state()

		for part in X.transpose(1,0,2,3,4):
			part_feat = self.model(part, layer_name=self.layer_name)
			feat = self.rnn(part_feat)

		pred = self.clf(feat)
		loss, accu = F.softmax_cross_entropy(pred, y), F.accuracy(pred, y)

		chainer.report({
			"loss": loss.data,
			"accuracy": accu.data,
		}, self)
		return loss

class PretrainedModelMixin(object):
	CHAINER_PRETRAINED = (
		chainer.links.model.vision.resnet.ResNetLayers,
		chainer.links.model.vision.vgg.VGG16Layers,
		chainer.links.model.vision.googlenet.GoogLeNet,
	)


	def __init__(self, n_classes=1000,
		pooling=PoolingType.Default, pooling_params={}, *args, **kwargs):

		if isinstance(self, PretrainedModelMixin.CHAINER_PRETRAINED):
			super(PretrainedModelMixin, self).__init__(
				pretrained_model=None, *args, **kwargs)
		else:
			super(PretrainedModelMixin, self).__init__(*args, **kwargs)

		if "input_dim" not in pooling_params:
			pooling_params["input_dim"] = self.meta.feature_size

		with self.init_scope():
			self.init_layers(n_classes)
			self.pool = PoolingType.new(pooling, **pooling_params)


	def load_for_finetune(self, weights, n_classes, **kwargs):
		"""
			The weights should be pre-trained on a bigger
			dataset (eg. ImageNet). The classification layer is
			reinitialized after all other weights are loaded
		"""
		self.load(weights)
		self.reinitialize_clf(n_classes, **kwargs)

	def load_for_inference(self, weights, n_classes, **kwargs):
		"""
			In this use case we are loading already fine-tuned
			weights. This means, we need to reinitialize the
			classification layer first and then load the weights.
		"""
		self.reinitialize_clf(n_classes, **kwargs)
		self.load(weights)

	def load(self, weights, strict=False):
		if weights not in [None, "auto"]:
			npz.load_npz(weights, self, strict=strict)

	def init_layers(self, n_classes):
		pass

	@property
	def clf_layer(self):
		clf_layer_name = self.meta.classifier_layers[-1]
		return getattr(self, clf_layer_name)

	@classmethod
	def prepare(cls, img, size=None):
		size = size or cls.meta.input_size
		if isinstance(size, int):
			size = (size, size)
		return cls.meta.prepare_func(img, size=size)

	@classmethod
	def prepare_back(cls, img):
		img = img.transpose(1,2,0).copy()
		img += cls.meta.mean.squeeze()
		img = img[..., ::-1].astype(np.uint8)
		return img

	def reinitialize_clf(self, n_classes,
		feat_size=None, initializer=None):
		if initializer is None or not callable(initializer):
			initializer = HeNormal(scale=1.0)

		clf_layer = self.clf_layer

		w_shape = (n_classes, feat_size or clf_layer.W.shape[1])
		clf_layer.W.data = np.zeros(w_shape, dtype=np.float32)
		clf_layer.b.data = np.zeros(w_shape[0], dtype=np.float32)
		initializer(clf_layer.W.data)

	# def load_pretrained(self, weights, n_classes):

	# 	layer_name = self.meta.classifier_layers[-1]
	# 	delattr(self, layer_name)
	# 	layer = L.Linear(self.meta.feature_size, n_classes)
	# 	setattr(self, layer_name, layer)

	# 	if weights not in [None, "auto"]:
	# 		npz.load_npz(weights, self)


	@property
	def functions(self):
		return OrderedDict(self._links)


	def __call__(self, X, layer_name=None):
		layer_name = layer_name or self.meta.classifier_layers[-1]
		caller = super(PretrainedModelMixin, self).__call__
		activations = caller(X, layers=[layer_name])
		if isinstance(activations, dict):
			activations = activations[layer_name]
		return activations


from chainer_addons.models.vgg import VGG19Layers
from chainer_addons.models.resnet import ResnetLayers, Resnet35Layers
from chainer_addons.models.inception import InceptionV3
