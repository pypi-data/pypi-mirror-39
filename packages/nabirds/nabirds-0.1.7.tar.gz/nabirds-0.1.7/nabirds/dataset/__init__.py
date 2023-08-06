from .mixins.reading import AnnotationsReadMixin, ImageListReadingMixin
from .mixins.parts import PartMixin, RevealedPartMixin, CroppedPartMixin

class Dataset(PartMixin, AnnotationsReadMixin):

	def get_example(self, i):
		im_obj = super(Dataset, self).get_example(i)
		return im_obj.as_tuple()
