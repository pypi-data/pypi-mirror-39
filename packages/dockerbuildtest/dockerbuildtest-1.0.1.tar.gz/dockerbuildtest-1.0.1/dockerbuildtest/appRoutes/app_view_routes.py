from flask import json

import flask


app = flask.Flask(__name__)
from ..handlers import docker_build_handler, default_views


@app.route('/')
def index():
    """load default home

    Returns:
        'template' -- 'will load default home'
    """
    return default_views.load_home()


@app.route("/build", methods=["POST"])
def build_image():
    """Build an image and return it. build_request must be set.

    Returns:
        object -- build_response
    """
    build_response = docker_build_handler.build_docker_image()

    if 'error' in build_response:
        response_data = json.dumps(build_response['error'])

        status_code = build_response['error']['status_code']

    else:
        response_data = json.dumps(build_response['response_data'])

        status_code = build_response['status_code']

    return app.response_class(
        response=response_data,
        status=status_code,
        mimetype='application/json'
    )


@app.route("/history", methods=["GET"])
def get_history():
    """Get build_image history

    Returns:
        object -- build_images logs
    """
    history_response = docker_build_handler.get_image_history()

    if 'error' in history_response:
        response_data = json.dumps(history_response['error'])

        status_code = history_response['error']['status_code']

    else:
        response_data = json.dumps(history_response['response_data'])

        status_code = history_response['status_code']

    return app.response_class(
        response=response_data,
        status=status_code,
        mimetype='application/json'
    )


@app.errorhandler(404)
def page_not_found(error):
    """To handle error

    Returns:
        object -- error_response
    """
    return app.response_class(
        response=json.dumps({
            'status_message': error.description or 'request url not found',
            'status_code': 404
        }),
        status=404,
        mimetype='application/json'
    )


@app.errorhandler(405)
def method_not_found(error):
    """To handle invalid routes

    Returns:
       object -- error_response
    """
    return app.response_class(
        response=json.dumps({
            'status_message': error.description or 'invalid method and url',
            'status_code': 405
        }),
        status=405,
        mimetype='application/json'
    )


@app.errorhandler(Exception)
def unhandled_exception(error):
    """To handle exception by code

    Returns:
       object -- error_response
    """

    message = 'exeception caught'

    for arg in error.args:
        message = '{} {}'.format(message, arg)

    return app.response_class(
        response=json.dumps({
            'status_message': message or 'server unavailable try after sometimes',
            'status_code': 500
        }),
        status=500,
        mimetype='application/json'
    )
