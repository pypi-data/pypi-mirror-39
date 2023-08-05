"""docker build handler provide implementation for build docker images and to get the build history
"""

from flask import request
from ..core.docker_build_client import DockerBuildClient

def build_docker_image():
    """This method will build a docker image

    Returns:
        object -- build response

    Raise:

        ValueError -- error while building image
        Exception -- raised when required fields are missing

    """
    try:
        try:
            build_request = request.get_json()
        except Exception as error: # pylint: disable=broad-except

            return {
                'error': {
                    'status_code': 400,
                    'status_message': 'build request json not found : {}'.format(error)
                }
            }

        # docker_client = DockerBuildClient(build_request['registry'])
        docker_client = DockerBuildClient()

        response = docker_client.build_image(build_request)

        return {
            'status_code': response['statusCode'] or 200,
            'response_data': response
        }

    except Exception as error: # pylint: disable=broad-except

        return {
            'error': {
                'status_code': 400,
                'status_message': 'build failed execution error : {}'.format(error)
            }
        }


def get_image_history():
    """Get build_image history

    Returns:
        object -- build_images logs
    """

    try:
        docker_client = DockerBuildClient()

        response = docker_client.history()

        if 'error' in response:
            return response

        return {
            'response_data': response,
            'status_code': response['statusCode'] or 200
        }

    except Exception as error: # pylint: disable=broad-except

        return {
            'error': {
                'status_code': 400,
                'status_message': 'execution error : {}'.format(error)
            }
        }
