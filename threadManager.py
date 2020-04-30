import threading

class ThreadManager():
	def __init__(self,worker, nthreads=1,args=(), kwargs=None):
		self._worker   = worker
		self._nthreads = nthreads
		self._args = args
		self._Threads = []
		self._running = False

	def _create_threads(self):
		for i in range(self._nthreads):
			t = threading.Thread(target=self._worker, args=self._args)
			self._Threads.append(t)

	def _run(self):
		for thread in self._Threads:
			thread.start()
		self._running = True

	def _stop(self):
		for thread in self._Threads:
			del thread
		del self._Threads

	def start(self):
		try:
			self._create_threads()
			self._run()
		except Exception as e:
			print(str(e))

	def stop(self):
		try:
			if self._running:
				self._stop()
		except Exception as e:
			print(str(e))
