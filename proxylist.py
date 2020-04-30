import re

ptHttp   = 0
ptSocks4 = 1
ptSocks5 = 2

class Proxy():
	def __init__(self,proxy,ptype=ptHttp):
		self.ptype = ptype
		self.proxy = proxy

	def get(self):
		if self.ptype == ptSocks4:
			prefix = "socks4//:"
		elif self.ptype == ptSocks5:
			prefix = "socks5//:"
		else:
			prefix = "http://"
		return (prefix+self.proxy)

class proxylist(list):
	def __init__(self,filename="", proxy_type=ptHttp):
		list.__init__(self)
		self._active = 0
		self._banned = 0
		self._ptype = proxy_type
		self.load_from_file(filename)

	def getActive(self):
		return self._active

	def getBanned(self):
		return self._banned

	def load_from_file(self, filename=""):
		if not len(filename):
			return

		fp    = open(filename, "r")
		lines = fp.readlines()
		fp.close()

		r = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\d{1,3}:\d{2,5}")

		for line in lines:
			line = r.split(line)[0]
			if len(line):
				proxy = Proxy(line,ptype=self._ptype)
				self.append(proxy.get())
				del proxy
