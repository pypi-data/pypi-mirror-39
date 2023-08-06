# -*- coding: utf-8 -*-

"""

Lazylog Python Client

Usage:

	>>> import lazylog
	>>> lazy = lazylog.Lazylog(channel='public/lazylog-python')
	>>> lazy.log('As easy as rolling off a log')

"""

import requests


DEFAULT_LAZYLOG_CHANNEL = 'public/lazylog-python'


class Lazylog(object):

	LAZYLOG_URL = 'https://www.lazylog.co/'

	def __init__(self, channel=None):
		self.channel = channel or DEFAULT_LAZYLOG_CHANNEL

		# Enable keep-alive and connection-pooling.
		self.session = requests.session()

	def log(self, text):
		url = self.LAZYLOG_URL + self.channel
		resp = self.session.post(url, data=text)
		return resp
