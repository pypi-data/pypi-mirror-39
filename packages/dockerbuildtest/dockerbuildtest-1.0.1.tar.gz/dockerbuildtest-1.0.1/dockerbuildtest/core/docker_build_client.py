"""This is a rabbitmq client class that contains  methods to publish and consume messages
"""

import logging
import json
import os
from datetime import datetime
from io import BytesIO
from pydash import remove
import docker

from .utils.validateSchema import validate_build_request

# create logs folder if doesnt exist
try:
    os.stat('logs')
except OSError:
    os.mkdir('logs')

# import logging.handlers as handlers
logging.basicConfig(
    filename='logs/buildagent.log',
    level=logging.DEBUG
)

CURRENT_DATE = datetime.now()
API_VERSION = '1.35'

LOGGER = logging.getLogger('dockerBuildClient')
LOGGER.setLevel(logging.DEBUG)


class DockerBuildClient:
    """DockerClient class will provide  method to build and run containers
    """

    def __init__(self):
        """This is DockerClient constructor in order to initilize configuration
        """

        # create console handler and set level to debug
        console_handler = logging.StreamHandler()

        # create formatter
        formatter = logging.Formatter(
            '[ %(levelname)s - %(name)s - %(asctime)s]- %(message)s \n')

        # add formatter to ch
        console_handler.setFormatter(formatter)

        # add ch to logger
        LOGGER.addHandler(console_handler)

        self.client = None

    # pylint: disable=R0201
    def connect(self):
        """This method will initialize the connection to docker engine

        Returns:
            object -- refernce to docker client
        """
        try:
            return docker.from_env()
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error(err)
            raise err

    # pylint: disable=R0201
    def build_image(self, build_request):
        """This method will build a docker image

        Returns:
            object -- build response
        """
        LOGGER.info("Running build image")

        try:
            build_logs = []
            build_log_list = []
            image_info = {}
            error = None

            # get all build logs
            try:
                with open('logs/build_logs.json') as logs:
                    build_logs = json.load(logs)
            except (OSError, ValueError):
                print('build_logs.json file not found')
                build_logs = []

            build_response_obj = {
                'requestId': build_request["requestId"],
                'name': build_request["name"],
                'version': build_request["version"],
                'imageName': build_request["imageName"],
                'toolId': build_request["requestId"],
                'status': 'building',
                'statusCode': 202,
                'message': "started image build"
            }
            # will add into build_logs file in logs with status building
            with open('logs/build_logs.json', mode='w') as logs:
                build_logs.append(build_response_obj)
                json.dump(build_logs, logs)

            image_info['validate_request'] = validate_build_request(build_request)

            if not image_info['validate_request']:
                LOGGER.error('Invalid request, failed schema validation')
                build_log_list.append('Invalid request object, schema validation failed')
                build_log_list.append(image_info['validate_request']['message'])
                error = {
                    'status': "failed",
                    'statusCode': 400,
                    'message': image_info['validate_request']['message'],
                    'buildLogs': build_log_list
                }
                return handle_response(build_response_obj, error)

            repo_url = build_request["imageName"]
            image_info['registry'] = False

            self.client = self.connect()
            print('--------------------hi')

            if 'registry' in build_request and build_request["registry"]["url"] and \
                    build_request["registry"]["username"] and build_request["registry"]["password"]:
                print('--------------------hello')
                repo_url = '{}/{}'.format(
                    build_request["registry"]["url"], build_request["imageName"])
                image_info['login_response'] = self.client.login(
                    registry=build_request["registry"]["url"],
                    username=build_request["registry"]["username"],
                    password=build_request["registry"]["password"]
                )
                LOGGER.info('Docker login response %s', image_info['login_response'])
                build_log_list.append(
                    'Docker login response {}'.format(image_info['login_response']))
                image_info['registry'] = True

            image_info['build_tag'] = '{}:{}'.format(repo_url, build_request["version"])

            LOGGER.info('Building Docker Image Tag %s', image_info['build_tag'])

            docker_file_stream = BytesIO(build_request["data"]["content"].encode('utf-8'))

            build_log_list.append('Building Docker Image Tag {}'.format(image_info['build_tag']))

            print('--------------build_response')
            print('--------------docker_file_stream', docker_file_stream)
            print('--------------image tag', image_info['build_tag'])
            print('--------------buildArgs', build_request["buildArgs"])

            build_response = self.client.images.build(
                fileobj=docker_file_stream,
                rm=True,
                forcerm=True,
                tag=image_info['build_tag'],
                buildargs=build_request["buildArgs"]
            )
            print('-2-------------build_response', build_response)

            image_info['build_log'] = build_response[1]
            image_info['image'] = build_response[0]
            image_info['image_history'] = []
            image_info['images'] = [image_info['build_tag']]

            for line in image_info['build_log']:
                if 'stream' in line:
                    build_log_list.append(line["stream"])
                elif 'aux' in line:
                    build_log_list.append(line["aux"])
                else:
                    build_log_list.append(line)

            for line in image_info['image'].history():
                image_info['image_history'].append(line)

            if image_info['registry']:
                LOGGER.info("Pushing image to repo: %s", repo_url)
                push_response = self.client.images.push(
                    repository=repo_url,
                    tag=build_request["version"],
                    auth_config=build_request["registry"],
                    stream=True
                )
                build_log_list.append(
                    "-------- Pushing Image: {}:{}".format(repo_url, build_request["version"]))
                image_info['images'].append(
                    "{}:{}".format(repo_url, build_request["version"])
                )
                for line in push_response:
                    resp_str = line.decode("utf-8")
                    build_log_list.append(resp_str)
                    if "errorDetail" in resp_str:
                        LOGGER.error("errorDetail in resp_str: [%s]", resp_str)
                        error = {
                            'status': "failed",
                            'statusCode': 500,
                            'message': resp_str,
                            'buildLogs': build_log_list
                        }
                        return handle_response(build_response_obj, error)

                LOGGER.info("Push Completed: %s", repo_url)

                if build_request['latestTag']:
                    LOGGER.info("Pushing image with latest Tag: %s", repo_url)
                    image_info['tag_response'] = image_info['image'].tag(repo_url, tag='latest')
                    build_log_list.append(
                        'Docker tag response  {}'.format(image_info['tag_response'])
                    )
                    push_response = self.client.images.push(
                        repository=repo_url,
                        tag="latest",
                        auth_config=build_request["registry"],
                        stream=True
                    )
                    build_log_list.append(
                        "-------- Pushing Image: {}:latest".format(repo_url))
                    image_info['images'].append("{}:latest".format(repo_url))

                    for line in push_response:
                        resp_str = line.decode("utf-8")
                        build_log_list.append(line.decode("utf-8"))
                        if "errorDetail" in resp_str:
                            LOGGER.error("push_response errorDetail [%s]", resp_str)
                            error = {
                                'status': "failed",
                                'statusCode': 500,
                                'message': resp_str,
                                'buildLogs': build_log_list
                            }
                            return handle_response(build_response_obj, error)

                    build_log_list.append(
                        "-------- Pushing Completed Image: {}:latest".format(repo_url))
                    # delete the image to untag the latest image
                    self.client.images.remove("{}:latest".format(repo_url))
                    build_log_list.append('Docker remove image to untag the latest image')

                    # delete_response = self.client.images.remove("{}:latest".format(repo_url))
                    # build_log_list.append(
                    #     'Docker remove latest image response  {}'.format(delete_response))
            else:
                build_log_list.append(
                    "-------- Push is not requested or check if \
                    request object contains required registry attributes")
                LOGGER.info(
                    "-------- Push is not requested check if request \
                    object contains required registry attributes")

            # delete the image
            self.client.images.remove("{}:{}".format(repo_url, build_request["version"]))
            build_log_list.append('Docker remove version image')

            # delete_response = self.client.images.remove(
            #     "{}:{}".format(repo_url, build_request["version"]))
            # build_log_list.append(
            #     'Docker remove version image response  {}'.format(delete_response))

            build_response_obj["images"] = image_info['images']
            build_response_obj["buildLogs"] = build_log_list
            build_response_obj["imageInfo"] = image_info['image'].attrs
            build_response_obj["imageLayers"] = image_info['image_history']

            return handle_response(build_response_obj)

        except docker.errors.BuildError as error:
            LOGGER.error('Exception in build docker.errors.BuildError: [%s]', error)
            build_log_list.append('Exception in build, failed to build. {}'.format(error))
            error = {
                'status': "failed",
                'statusCode': 500,
                'message': 'Exception in build, failed to build. {}'.format(error),
                'buildLogs': build_log_list
            }
            return handle_response(build_response_obj, error)

        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error('Exception in build:[%s]', error)
            build_log_list.append('Generic Exception in build, failed to build. {}'.format(error))
            error = {
                'status': "failed",
                'statusCode': 500,
                'message': 'Generic Exception in build: [{}]'.format(error),
                'buildLogs': build_log_list
            }
            return handle_response(build_response_obj, error)

    # pylint: disable=R0201
    def history(self):
        """Get build_image history with count

        Returns:
            object -- build_images logs
        """

        try:
            LOGGER.info("Running history")
            # get all build logs
            try:
                with open('logs/build_logs.json') as logs:
                    build_logs = json.load(logs)
            except (OSError, ValueError):
                print('build_logs.json file not found')
                build_logs = []

            history_response = {}
            history_response['builds_count'] = len(build_logs)
            history_response['builds'] = build_logs

            return {
                "data": history_response,
                "statusCode": 200
            }

        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error('Exception while getting history: [%s]', error)
            raise error



def handle_response(build_res_obj, error_data=None):
    """handle_response will update log with end result and return result dict

    Arguments:
        build_res_obj {dict} -- image build_response object

    Keyword Arguments:
        error_data {dict} -- need to update build_response (default: {None})

    Returns:
        dict -- image build response
    """

    # getting all logs
    with open('logs/build_logs.json') as logs:
        build_logs = json.load(logs)

    # will update the last log status failed, since it doesn't match with schema
    with open('logs/build_logs.json', mode='w') as logs:
        remove(build_logs, lambda log: log['requestId'] == build_res_obj["requestId"])
        if error_data:
            build_res_obj['status'] = error_data['status']
            build_res_obj['statusCode'] = error_data['statusCode']
            build_res_obj['message'] = error_data['message']
            build_res_obj['buildLogs'] = error_data['buildLogs']
        else:
            build_res_obj['status'] = 'success'
            build_res_obj['statusCode'] = 200

        build_logs.append(build_res_obj)
        json.dump(build_logs, logs)
    return {
        "build_result": build_res_obj,
        "statusCode": error_data['statusCode'] if error_data else 200
    }
