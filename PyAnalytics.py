import subprocess 

server = "http://localhost:5000/"
log = server+"log"
register = server+"register"

class PyAnalytics:
	
	def __init__(self, key):
		self.key = key

	def test_connection(self):
		print "test_connection"

	def log_use(self, string):
		return subprocess.check_output(['curl', log, '-d', 'log_type=use&key='+self.key+'&text='+string, '-X', 'PUT'])

	def log_error(self, string):
		print "log error"

analytics = PyAnalytics("141107214506facebook")
print analytics.log_use("dbg .")
