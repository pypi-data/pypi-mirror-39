from imageio import imread
from os.path import isfile

import copy
import numpy as np

from . import utils

def should_have_parts(func):
	def inner(self, *args, **kwargs):
		assert self.has_parts, "parts are not present!"
		return func(self, *args, **kwargs)
	return inner

class ImageWrapper(object):
	def __init__(self, im_path, label, parts=None, mode="RGB"):
		if isinstance(im_path, str):
			assert isfile(im_path), "Image \"{}\" does not exist!".format(im_path)
			self.im = imread(im_path, pilmode=mode)
		else:
			self.im = im_path

		self.label = label
		self.parts = parts

		self.parent = None

	def as_tuple(self):
		return self.im, self.parts, self.label

	def copy(self):
		new = copy.deepcopy(self)
		new.parent = self
		return new


	def crop(self, x, y, w, h):
		result = self.copy()
		result.im = self.im[y:y+h, x:x+w]
		if self.has_parts:
			result.parts[:, 1] -= x
			result.parts[:, 2] -= y
		return result

	@should_have_parts
	def hide_parts_outside_bb(self, x, y, w, h):
		idxs, (xs,ys) = self.visible_part_locs()
		f = np.logical_and
		mask = f(f(x <= xs, xs <= x+w), f(y <= ys, ys <= y+h))
		result = self.copy()
		result.parts[:, -1] = mask.astype(self.parts.dtype)

		return result

	def uniform_parts(self, ratio):
		result = self.copy()
		result.parts = utils.uniform_parts(self.im, ratio=ratio)
		return result

	@should_have_parts
	def select_parts(self, idxs):
		result = self.copy()

		result.parts[:, -1] = 0
		result.parts[idxs, -1] = 1

		return result

	@should_have_parts
	def select_random_parts(self, rnd, n_parts):

		idxs, xy = self.visible_part_locs()
		rnd_idxs = utils.random_idxs(idxs, rnd=rnd, n_parts=n_parts)
		return self.select_parts(rnd_idxs)

	@should_have_parts
	def visible_crops(self, ratio):
		return utils.visible_crops(self.im, self.parts, ratio=ratio)

	@should_have_parts
	def visible_part_locs(self):
		return utils.visible_part_locs(self.parts)

	@should_have_parts
	def reveal_visible(self, ratio):
		_, xy = self.visible_part_locs()
		result = self.copy()
		result.im = utils.reveal_parts(self.im, xy, ratio=ratio)
		return result

	@should_have_parts
	def part_crops(self, ratio):
		crops = self.visible_crops(ratio)
		idxs, _ = self.visible_part_locs()
		result = self.copy()
		result.im = crops[idxs]
		return result

	@property
	def has_parts(self):
		return self.parts is not None

