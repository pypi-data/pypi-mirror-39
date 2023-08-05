# -*- coding: utf-8 -*-
class LevelFilter(object):
	def __init__(self, level):
		self.level = level

	def filter(self, record):
		return record.levelno == self.level