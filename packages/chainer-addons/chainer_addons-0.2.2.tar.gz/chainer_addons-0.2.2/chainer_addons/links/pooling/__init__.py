from .compact_bilinear import CompactBilinearPooling
from .alpha_pooling import AlphaPooling
from .global_avg import GlobalAveragePooling

from cvargparse.utils.enumerations import BaseChoiceType

class PoolingType(BaseChoiceType):
	AVG = GlobalAveragePooling
	CBIL = CompactBilinearPooling
	ALPHA = AlphaPooling
	Default = AVG

	@classmethod
	def new(cls, pool_type, **kwargs):
		pool_cls = cls.get(pool_type).value
		return pool_cls(**kwargs)

