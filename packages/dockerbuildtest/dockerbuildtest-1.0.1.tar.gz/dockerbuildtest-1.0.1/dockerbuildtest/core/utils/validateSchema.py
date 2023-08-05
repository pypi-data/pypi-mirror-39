from jsonschema import validate
import jsonschema


def validate_build_request(build_request):
    """To validate build request object

    Returns:
        object -- build_request

    Raises:
        ValidationError -- raised if required keys are missing
        in the build_request
    """

    request_schema = {
        "type": "object",
        "properties": {
            "requestId": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "version": {
                "type": "string"
            },
            "imageName": {
                "type": "string"
            },
            "data": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string"
                    },
                    "contentType": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    },
                    "dockerFile": {
                        "type": "string"
                    }
                },
                "required": ["content"]
            },
            "latestTag": {
                "type": "boolean"
            },
            "tags": {
                "type": "array"
            },
            "registry": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string"
                    },
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    }
                },
                "required": ["url"]
            },
            "buildArgs": {
                "type": "object",
                "properties": {
                    "VERSION": {
                        "type": "string"
                    },
                    "PROJECT_HOME": {
                        "type": "string"
                    }
                }
            },
            "push": {
                "type": "boolean"
            }
        },
        "required": [ "imageName", "version", "data", "name", "buildArgs"]
    }

    try:
        validate(build_request, request_schema)
        return True
    except jsonschema.exceptions.ValidationError as validateErr:
        validateErr = '{}'.format(validateErr)
        validateErr = validateErr.split('\n')

        return {
            "message": validateErr[2]+validateErr[0],
            "status": "failed",
            "statusCode": 400
        }
