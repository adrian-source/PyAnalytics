PyAnalytics
===========

Python class a flask component that can be used to track usage, execution count, and errors of a python script. This is built with intention of being used in offices where custom scripts are being created and used by engineers.

*INSTALLATION:

1. Install the following flask components with pip

flask/bin/pip install flask==0.9

flask/bin/pip install sqlalchemy==0.7.9

flask/bin/pip install flask-sqlalchemy==0.16

flask/bin/pip install sqlalchemy-migrate==0.7.2

flask/bin/pip install flask-whooshalchemy==0.55a

flask/bin/pip install flask-wtf==0.8.4

flask/bin/pip install flask-restful

2. Setup the databse (see comments inside flask-run.py)

3. Run the server with the following command

./flask-run.py

4. Alter the web server's address in PyAnalytics.py
