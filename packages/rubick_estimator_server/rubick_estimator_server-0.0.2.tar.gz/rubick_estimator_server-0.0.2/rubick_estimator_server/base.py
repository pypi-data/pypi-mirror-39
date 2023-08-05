from flask import Flask, jsonify

server = Flask(__name__)


def estimator(func):
	@server.route('/predict/<path:text>')
	def __decorator(text):
		response = server.make_response(jsonify(data=func(text), code=0, msg="success"))
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET'
		response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
		return response

	return __decorator
