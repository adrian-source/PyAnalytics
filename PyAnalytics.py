import subprocess, os, socket

server = "http://localhost:5000/"
log = server+"log"
register = server+"register"

class PyAnalytics:
	
	def __init__(self, key):
		self.key = key

	def test_connection(self):
		print "test_connection"

	def log_use(self, string):
		result = subprocess.Popen(['curl', log, '-s', '-d', 'log_type=use&hostname='+socket.gethostname()+'&key='+self.key+'&text='+string, '-X', 'PUT'], stdout=open(os.devnull, 'wb'))

	def log_error(self, string):
		result = subprocess.Popen(['curl', log, '-s', '-d', 'log_type=error&hostname='+socket.gethostname()+'&key='+self.key+'&text='+string, '-X', 'PUT'], stdout=open(os.devnull, 'wb'))


