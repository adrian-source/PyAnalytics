
import PyAnalytics
import random, string
from time import sleep

key = "" # PUT YOUR KEY HERE
pyanal = PyAnalytics.PyAnalytics(key)

for i in range(0, 1000):
	cmd = ''.join(random.choice(string.ascii_uppercase) for i in range(40))
	pyanal.log_use(cmd)
	sleep(0.01)

