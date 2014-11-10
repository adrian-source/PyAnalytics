#!flask/bin/python
from app import app
from flask import Flask, request
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
import datetime, os.path
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

class Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(20), unique=True)
	email = db.Column(db.String(20), unique=False)
	appname = db.Column(db.String(20), unique=False)
	created = db.Column(db.DateTime)

	def __init__(self, key, appname, email):
		self.key = key
		self.appname = appname
		self.email = email
		self.created = datetime.datetime.utcnow()
		

	def __repr__(self):
		return "<Key %r>" % self.email

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
	text = db.Column(db.String(100), unique=False)
	log_type = db.Column(db.String(10), unique=False)
	hostname = db.Column(db.String(20), unique=False)
	created = db.Column(db.DateTime)

	def __init__(self, log_type, key_id, text, hostname):
		self.log_type = log_type 
		self.key_id = key_id
		self.text = text
		self.hostname = hostname
		self.created = datetime.datetime.utcnow()

	def __repr__(self):
		return "<Log %r>" % self.text

db.create_all()
'''
# USE THIS TO CREATE DATABASE
from config import SQLLCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
'''

'''
/log commands
Used to add and retrieve log entries for the provided app key.
'''
class PyAnalyticsAdd(Resource):
    def get(self):
	key = request.form["key"]
	key_db = Key.query.filter_by(key=key).first()
	if key_db != None:
		count = Log.query.filter_by(key_id = key_db.id).count()
		return {'count': count}
	else:
		return {'status': 400, 'message': 'invalid key'}

    '''
    @param  log_type   Can be either 'use' or 'error'
    @param  key        Valid key for the application
    @param  text       String to be stored in the system
    @param  hostname   Hostname of the user
    '''
    def put(self):
	log_type = request.form["log_type"]
	key = request.form["key"]
	text = request.form["text"]
	hostname = request.form["hostname"]
        
	# validate key
	key_db = Key.query.filter_by(key=key).first()
	if key_db != None:
		try:
			log = Log(log_type, key_db.id, text, hostname)
			db.session.add(log)
			db.session.commit()
		except IntegrityError:
			return {'status': 400, 'message': 'database returned an error'}
	else:
		return {'status': 400, 'message': 'invalid key'}
		
        return 200

'''
/register commands
Used to create and retrieve keys needed to use this service.
'''
class PyAnalyticsRegister(Resource):
	'''
	Get a list of registered keys for an email address
	@param	email
	'''
	def get(self):
		email = request.form["email"]
		keys = Key.query.filter_by(email=email).all()
		if keys != None:
			jsonresp = "{"
			for key in keys:
				jsonresp += "%s: %s, " % (key.email, key.key)
			jsonresp = jsonresp[:-2] + "}"
			return jsonresp
		return "No entry found for "+email
	
	'''
	Register for a new key
	@param	appname	Name of your application
	@param	email	Your real email address
	
	@return	{key:<new key>}
	'''
	def put(self):
		appname = request.form["appname"]
		email = request.form["email"]
		datenow = datetime.datetime.now()
		new_key = datenow.strftime("%y%m%d%H%M%S")+appname
		try:
			key = Key(new_key, appname, email)
			db.session.add(key)
			db.session.commit()
		except IntegrityError:
			return {'status': 400, 'message': 'database returned an error'}
		
		return "{key:%s}" % new_key

api.add_resource(PyAnalyticsAdd, '/log')
api.add_resource(PyAnalyticsRegister, '/register')

@app.route('/logs/<string:key>')
def logs(key):
	key_db = Key.query.filter_by(key=key).first()
	if key_db != None:
		logs = Log.query.filter_by(key_id=key_db.id).order_by(desc(Log.created)).all()
		result = key_db.key +  " - " + key_db.appname + " - " + key_db.email + "<br><br>"
		count = 0
		for log in logs:
			count += 1
			result += str(count) + ". " + str(log.created) + " " + log.text+"<br>"
		return result
	else:
		return "invalid key"

@app.route('/keys/<string:email>')
def keys(email):
	keys = Key.query.filter_by(email=email).all()
	result = "Found "+str(len(keys))+" entries for email"+email+"<br><br>"
	for key in keys:
		result += "<a href='/logs/"+key.key+"'>"+key.key + "</a> - " + key.appname + "<br>"
	return result

if __name__ == '__main__':
    app.run(debug=True)

