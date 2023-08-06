import numpy as np, chainer
from chainer.training import extension

class ContiniousLearningRate(extension.Extension):
	trigger = 1, 'epoch'

	def _get_optimizer(self, trainer):
		return self._optimizer or trainer.updater.get_optimizer('main')

	def initialize(self, trainer):
		self.set_lr(trainer, self._lr)

	def set_lr(self, trainer, value):
		optimizer = self._get_optimizer(trainer)
		setattr(optimizer, self._attr, max(value, self._target))

	def __init__(self, attr, lr, target, epochs, offset, optimizer=None):
		super(ContiniousLearningRate, self).__init__()
		self._optimizer = optimizer
		self._attr = attr
		self._lr = lr
		self._target = target
		self._epochs = epochs
		self._offset = offset

	@property
	def factor(self):
		raise NotImplementedError

	def new_lr(self, epoch):
		raise NotImplementedError

	def __call__(self, trainer):
		if trainer.updater.epoch - self._offset < 0: return
		if trainer.updater.epoch - self._offset > self._epochs: return
		self.set_lr(trainer, self.new_lr(trainer.updater.epoch - self._offset))


class ExponentialLearningRate(ContiniousLearningRate):

	@property
	def factor(self):
		return pow(10, np.log10(self._target / self._lr) / self._epochs)

	def new_lr(self, epoch):
		return self._lr * self.factor ** epoch

class LinearLearningRate(ContiniousLearningRate):

	def new_lr(self, epoch):
		return self._lr - (self.factor * epoch)

	@property
	def factor(self):
		return (self._lr - self._target) / self._epochs
