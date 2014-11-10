
import PyAnalytics
import random, string, os
from time import sleep
import json

key = "141109230052app4" # PUT YOUR KEY HERE
pyanal = PyAnalytics.PyAnalytics(key)

result = json.loads(os.popen('curl http://localhost:5000/log -d "key='+key+'" -X GET').read())
count = result["count"]

for i in range(0, 1000):
	cmd = ''.join(random.choice(string.ascii_uppercase) for i in range(40))
	pyanal.log_use(cmd)
	sleep(0.01)
	result = json.loads(os.popen('curl http://localhost:5000/log -s -d "key='+key+'" -X GET').read())
	if result["count"] == count+1:
		count += 1
		print count
	else:
		print "FAIL! "+str(count)
		break
