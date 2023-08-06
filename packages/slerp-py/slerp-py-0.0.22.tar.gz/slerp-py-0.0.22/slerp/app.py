import codecs
import json
from urllib.parse import urlencode

from flask import Flask
from flask import request
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

from .consul import Consulate
from .exception import ValidationException, CoreException
from .logger import logging
from .response import JsonResponse

log = logging.getLogger(__name__)

DEFAULT_CONFIG = 'config.json'


# if not os.path.exists(DEFAULT_CONFIG):
# 	raise RuntimeError('please create config.json file in your project root folder')


def init_apps(configuration=None):
	apps = Flask(__name__)
	try:
		consul = Consulate(app=apps)
		consul.load_config(namespace=configuration['namespace'])
		c = configuration
		c.pop('namespace')
		c.pop('log_file')
		consul.register(**c)
	except Exception as e:
		log.info("Consulate is not running")
		pass
	return apps


config = None
try:
	json_file = open(DEFAULT_CONFIG, 'rb')
	reader = codecs.getreader('utf-8')
	config = json.load(reader(json_file))
	json_file.close()
except:
	log.info('No consul configuration found')
	pass

app = init_apps(config)
db = SQLAlchemy(app=app)
cache = Cache(app, config=app.config)
app.response_class = JsonResponse


@app.errorhandler(Exception)
# noinspection PyTypeChecker
def handle_error(error):
	log.error(error, exc_info=True)
	msg = {'status': 'FAIL'}
	if type(error) is TypeError:
		msg['message'] = 'type.error'
	elif type(error) is ValidationException:
		msg['message'] = error.message
		if error.key is not None:
			msg['key'] = error.key
			pass
	elif type(error) is CoreException:
		msg['message'] = error.message
	else:
		message = [str(x) for x in error.args]
		msg['message'] = message
	return msg


def cached_key():
	path = request.path
	args = dict(request.args)
	if args:
		if 'access_token' in args:
			args.pop('access_token')
		return path + '?' + urlencode(args, encoding='utf-8', doseq=True)
	return path


@app.before_request
def return_cached():
	if request.method == 'GET':
		response = cache.get(cached_key())
		if response:
			log.info("Using cache for %s", request.path)
			return response


@app.after_request
def session_commit(response):
	if request.method == 'GET' and type(response) == JsonResponse:
		cache_key = cached_key()
		log.info("Cache Key : %s", cache_key)
		try:
			cache.set(cache_key, response, app.config['CACHE_TIMEOUT'] if 'CACHE_TIMEOUT' in app.config else 300)
			return response
		except Exception:
			log.info("Failed to create cache for %s", cache_key)
	if 'AUTO_ROLLBACK' in app.config and app.config['AUTO_ROLLBACK']:
		db.session.rollback()
	else:
		try:
			db.session.commit()
		except Exception:
			db.session.rollback()
			raise
	return response


def run(**kwargs):
	if 'SERVER_PORT' in app.config:
		kwargs.update({'port': app.config['SERVER_PORT']})
	if 'SERVER_HOST' in app.config:
		kwargs.update({'host': app.config['SERVER_HOST']})
	else:
		kwargs.update({'host': '0.0.0.0'})
	app.run(**kwargs)
