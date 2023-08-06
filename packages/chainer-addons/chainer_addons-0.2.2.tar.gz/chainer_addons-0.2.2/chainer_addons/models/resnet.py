import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F

from chainer.serializers import npz
from chainer.links.model.vision.resnet import prepare, BuildingBlock
from functools import partial

from chainer_addons.models import PretrainedModelMixin


class ResnetMixin(PretrainedModelMixin):

	@property
	def _links(self):
		links = [
				('conv1', [self.conv1, self.bn1, F.relu]),
				('pool1', [partial(F.max_pooling_2d, ksize=3, stride=2)]),
				('res2', [self.res2]),
				('res3', [self.res3]),
				('res4', [self.res4]),
				('res5', [self.res5]),
				('pool5', [self.pool])]
		if hasattr(self, "fc6"):
			links +=[
				('fc6', [self.fc6]),
				('prob', [F.softmax]),
			]

		return links


class ResnetLayers(ResnetMixin, L.ResNet50Layers):

	class meta:
		classifier_layers = ["fc6"]
		conv_map_layer = "res5"
		feature_layer = "pool5"
		feature_size = 2048
		n_conv_maps = 2048
		input_size = 448
		mean = np.array([103.063,  115.903,  123.152], dtype=np.float32).reshape(3,1,1)

		prepare_func = prepare

	# def __init__(self, pretrained_model, n_classes, *args, **kwargs):
	# 	super(ResnetLayers, self).__init__(
	# 		pretrained_model=pretrained_model if pretrained_model == "auto" else None,
	# 		*args, **kwargs)

	# 	with self.init_scope():
	# 		self.load_pretrained(pretrained_model, n_classes)



class Resnet35Layers(ResnetMixin, chainer.Chain):

	class meta:
		classifier_layers = ["fc6"]
		conv_map_layer = "res5"
		feature_layer = "pool5"
		feature_size = 2048
		n_conv_maps = 2048
		input_size = 448
		mean = np.array([103.063,  115.903,  123.152], dtype=np.float32).reshape(3,1,1)

		prepare_func = prepare


	def init_layers(self, n_classes, **kwargs):
		self.conv1 = L.Convolution2D(3, 64, 7, 2, 3, **kwargs)
		self.bn1 = L.BatchNormalization(64)
		self.res2 = BuildingBlock(2, 64, 64, 256, 1, **kwargs)
		self.res3 = BuildingBlock(3, 256, 128, 512, 2, **kwargs)
		self.res4 = BuildingBlock(3, 512, 256, 1024, 2, **kwargs)
		self.res5 = BuildingBlock(3, 1024, 512, 2048, 2, **kwargs)
		self.fc6 = L.Linear(2048, n_classes)

	# def __init__(self, pretrained_model, n_classes, *args, **kwargs):
	# 	super(Resnet35Layers, self).__init__(*args, **kwargs)

	# 	if pretrained_model not in [None, "auto"]:
	# 		npz.load_npz(pretrained_model, self)

	def __call__(self, x, layers=['prob']):
		h = x
		activations = {}
		target_layers = set(layers)
		for key, funcs in self.functions.items():
			if len(target_layers) == 0:
				break
			for func in funcs:
				h = func(h)
			if key in target_layers:
				activations[key] = h
				target_layers.remove(key)
		return activations
