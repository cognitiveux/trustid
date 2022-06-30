from rest_framework import serializers
from drf_yasg import openapi
from .logging import logger as log
from .models import *

"""
Dictionaries included in the module are useful when someone wants to modify the documentation of the responses
For modifying the possible responses of a view:
1.First modify the response_types list in your view class and add a list in the 2d list
that agrees with STATUS_CODES which lives in this file.
2.Then in VIEWS_DESCRIPTION find the key of this class(or add it) and add your status_code in the list
and also add your keys that you want to be returned with this status_code in the response body.
3.For adding a new description for a response field in the response body:
Add in GENERAL_DESCRIPTIONS the key name and the description of the key
Add in FIELD_TYPES the type of the field
3.1.If it has many possible values add in ENUM_VARIABLES all the possible values
"""


"""
RESOURCE_NAMES dict provides a list with all the possible resource names that are related with
keys starting with resource_* in STATUS_CODES dictionary
"""
RESOURCE_NAMES = {
    'enrollment': "Enrollment",
    'examination': "Examination",
    'image': "Image",
    'jwt': "JSON Web Token",
    'process': "Process",
    'user': "User",
    'version': "Version",
}


"""
Different types of variables which can be returned in response
"""
RESPONSE_TYPES = {
    'bool': '\<Boolean\>',
    'float': '\<Float\>',
    'int': '\<Integer\>',
    'dict': '\<Dictionary\>',
    'array': '\<Array\>',
}

"""
Classnames for which the bad request dict should not be generated
"""
IGNORE_BAD_REQUEST = []


"""
Contains different possible responses with their status code and message
"""
STATUS_CODES = {
    'success': {
        'code': 200,
        'msg': "Success"
    },
    'resource_created_return_obj': {
        'code': 201,
        'msg': "{} has been created successfully. The value is returned in `resource_obj`."
    },
    'resource_created_return_str': {
        'code': 201,
        'msg': "{} has been created successfully. The value is returned in `resource_str`."
    },
    'bad_formatted_json': {
        'code': 400,
        'msg': "Json parse failed"
    },
    'bad_request': {
        'code': 400,
        'msg': "Bad request (Invalid data) - Any missing, already existing or bad formatted fields will be returned"
    },
    'unauthorized': {
        'code': 401,
        'msg': "Unauthorized - The request lacks valid authentication credentials."
    },
    'resource_not_allowed': {
        'code': 403,
        'msg': "Forbidden. You are not allowed to access this resource."
    },
    'resource_not_found': {
        'code': 404,
        'msg': "{} not found"
    },
    'method_not_allowed': {
        'code': 405,
        'msg': "Method not allowed"
    },
    'unsupported_media_type': {
        'code': 415,
        'msg': "Unsupported media type"
    },
    'internal_server_error': {
        'code': 500,
        'msg': "Internal server error"
    },
}


"""
Responses that contain a message with a variable.
The type of the variable is described in the message
"""
VARIABLE_RESULTS = {
    'request_limit_exceeded': {
        'code': 422,
        'msg': "Request limit exceeded. Try again in %s seconds",
        'type': [RESPONSE_TYPES['int']],
    }
}


"""
Description of various keys that appear in the response body
"""
GENERAL_DESCRIPTIONS = {
    'alerts': "The alerts detected for the individual.",
    'already_exists_fields': "Any field that is unique and already exists, will be returned in the list",
    'bad_formatted_fields': "Any field that is not in the correct format will be returned in the list",
    'email': "The email of the individual",
    'enrolled_students': "The list of students' emails enrolled for this examination",
    'error_details': "A dictionary that contains descriptive information " \
        "about the validation errors in the form of key-value pairs. " \
        "Each key is a string that corresponds to the problematic field " \
        "and the associated value is a list of strings that contains the error details. " \
        "If a JSON parse error occurred, there will be only one key named `json`.",
    'exam_id': "The ID of the examination",
    'macos_version': "The version of MacOS app",
    'message': "A general message description",
    'exam_name': "The name of the examination",
    'missing_required_fields': "The missing required fields are returned as a list",
    'name': "The name of the individual",
    'privacy_policy': "The privacy policy of the examination",
    'extra_details': "Extra details regarding the resource",
    'resource': "A value associated with that resource",
    'resource_array': "An array with all the available data",
    'resource_bool': "A boolean value associated with the name of the resource",
    'resource_dict': "A dictionary result with all the available data",
    'resource_name': "The name of the resource",
    'resource_obj': "A dictionary that contains the JWT " \
        "in the form of key-value pairs. " \
        "The key `access` is a string that corresponds to the JWT access token " \
        "and the key `refresh` is a string that corresponds to the JWT refresh token. ",
    'resource_str': "A string value associated with the resource_name",
    'scheduled_date': "The scheduled date of the examination",
    'server_version': "The version of the backend server",
    'status': "The status of the examination",
    'surname': "The surname of the individual",
    'timestamp': "The current server's timestamp",
    'verification_status': "The status of the verification",
    'windows_version': "The version of Windows app",
}

"""
Description for responses that need to be custom.
    key: classname
    value: the openapi dictionary specification for describing a response body
"""
CUSTOM_RESPONSES = {
    'InstructorListExam': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_array': {
                    'type': openapi.TYPE_ARRAY,
                    'items': {
                        'type': openapi.TYPE_OBJECT,
                        'properties': {
                            'enrolled_students': {
                                'type': openapi.TYPE_ARRAY,
                                'description': GENERAL_DESCRIPTIONS.get('enrolled_students'),
                                'items': {
                                    'type': openapi.TYPE_OBJECT,
                                    'properties': {
                                        'alerts': {
                                            'type': openapi.TYPE_STRING,
                                            'description': GENERAL_DESCRIPTIONS.get('alerts')
                                        },
                                        'email': {
                                            'type': openapi.TYPE_STRING,
                                            'description': GENERAL_DESCRIPTIONS.get('email')
                                        },
                                        'name': {
                                            'type': openapi.TYPE_STRING,
                                            'description': GENERAL_DESCRIPTIONS.get('name')
                                        },
                                        'surname': {
                                            'type': openapi.TYPE_STRING,
                                            'description': GENERAL_DESCRIPTIONS.get('surname')
                                        },
                                        'verification_status': {
                                            'type': openapi.TYPE_STRING,
                                            'description': GENERAL_DESCRIPTIONS.get('verification_status'),
                                            'enum': [
                                                VerificationStatusModel.PENDING,
                                                VerificationStatusModel.REQUESTED_MANUAL_APPROVAL,
                                                VerificationStatusModel.VERIFIED,
                                            ]
                                        },
                                    }
                                }
                            },
                            'exam_id': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('exam_id')
                            },
                            'name': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('exam_name')
                            },
                            'status': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('status')
                            },
                            'scheduled_date': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('scheduled_date')
                            },
                            'privacy_policy': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('privacy_policy')
                            }
                        }
                    }
                },
                'resource_name': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('resource_name')
                },
            }
        }
    },
    'StudentListExam': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_array': {
                    'type': openapi.TYPE_ARRAY,
                    'items': {
                        'type': openapi.TYPE_OBJECT,
                        'properties': {
                            'exam_id': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('exam_id')
                            },
                            'name': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('exam_name')
                            },
                            'status': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('status')
                            },
                            'scheduled_date': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('scheduled_date')
                            },
                            'privacy_policy': {
                                'type': openapi.TYPE_STRING,
                                'description': GENERAL_DESCRIPTIONS.get('privacy_policy')
                            }
                        }
                    }
                },
                'resource_name': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('resource_name')
                },
            }
        }
    },
    'TrustidVersion': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_dict': {
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'server_version': {
                            'type': openapi.FORMAT_FLOAT,
                            'description': GENERAL_DESCRIPTIONS.get('server_version')
                        },
                        'windows_version': {
                            'type': openapi.FORMAT_FLOAT,
                            'description': GENERAL_DESCRIPTIONS.get('windows_version')
                        },
                        'macos_version': {
                            'type': openapi.FORMAT_FLOAT,
                            'description': GENERAL_DESCRIPTIONS.get('macos_version')
                        },
                        'timestamp': {
                            'type': openapi.FORMAT_FLOAT,
                            'description': GENERAL_DESCRIPTIONS.get('timestamp')
                        }
                    }
                },
                'resource_name': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('resource_name')
                },
            }
        }
    },
}

"""
Associates field name from VIEWS_DESCRIPTION dictionary with resource type
"""
FIELD_TYPES = {
    'already_exists_fields': openapi.TYPE_ARRAY,
    'bad_formatted_fields': openapi.TYPE_ARRAY,
    'error_details': openapi.TYPE_OBJECT,
    'extra_details': openapi.TYPE_STRING,
    'message': openapi.TYPE_STRING,
    'missing_required_fields': openapi.TYPE_ARRAY,
    'resource': openapi.TYPE_STRING,
    'resource_array': openapi.TYPE_ARRAY,
    'resource_bool': openapi.TYPE_BOOLEAN,
    'resource_dict':openapi.TYPE_OBJECT,
    'resource_name': openapi.TYPE_STRING,
    'resource_obj': openapi.TYPE_OBJECT,
    'resource_str': openapi.TYPE_STRING,
}


"""
Describes for each class it's enum variables and the values they can take
"""
ENUM_VARIABLES = {
    'AddExam': {},
    'DetectLowContrast': {},
    'EnrollStudents': {},
    'ExamConditionUpdate': {},
    'HeadPoseClassification': {},
    'InstructorListExam': {},
    'InstructorManualApproveStudent': {
        'resource_name': ['user', 'examination',]
    },
    'Login': {},
    'Monitoring': {},
    'RefreshToken': {},
    'RegisterUser': {},
    'SampleAuthenticated': {},
    'StudentCheckupProcess': {},
    'StudentCheckVerificationStatus': {
        'resource_name': ['user', 'examination',]
    },
    'StudentIdentification': {},
    'StudentListExam': {},
    'StudentRequestManualApproval': {
        'resource_name': ['user', 'examination',]
    },
    'StudentSubmitFeedback': {
        'resource_name': ['user', 'examination',]
    },
    'TrustidVersion': {},
    'UpdateExamDetails': {
        'resource_name': ['user', 'examination',]
    },
}


"""
Contains for each view the different status codes that can return and their corresponding
keys
"""
VIEWS_DESCRIPTION = {
    'AddExam': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'DetectLowContrast': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_bool',
                'extra_details',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'EnrollStudents': [
        {
            'status_code': [200],
            'variables': [
                'message',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'ExamConditionUpdate': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'HeadPoseClassification': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_str',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'InstructorListExam': [
        {
            'status_code': [200],
            'variables': [], # Override by CUSTOM_RESPONSES
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'InstructorManualApproveStudent': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'Login': [
        {
            'status_code': [201],
            'variables': [
                'message',
                'resource_name',
                'resource_obj',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
    ],
    'Monitoring': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'RefreshToken': [
        {
            'status_code': [201],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'error_details'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'RegisterUser': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'SampleAuthenticated': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentCheckupProcess': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentCheckVerificationStatus': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_bool',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentIdentification': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentListExam': [
        {
            'status_code': [200],
            'variables': [], # Override by CUSTOM_RESPONSES
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentRequestManualApproval': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'StudentSubmitFeedback': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'TrustidVersion': [
        {
            'status_code': [200],
            'variables': [], # Override by CUSTOM_RESPONSES
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'UpdateExamDetails': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [401, 403, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
}


def _wrong_method_schema():
    """
    Returns:
        an openapi.Schema which corresponds to wrong method response
    """
    message_key = 'message'
    schema_dict = {
        'type':openapi.TYPE_OBJECT,
        'title':'Response body for status code 405',
        'description':'Following keys are returned as json',
        'properties':{
            message_key:{
                'type': FIELD_TYPES[message_key],
                'description': GENERAL_DESCRIPTIONS[message_key],
            },
        }
    }
    return openapi.Schema(**schema_dict)


def _bad_request_schema():
    '''
    Returns:
        openapi.Schema which corresponds to a bad request
    '''
    missing_required_fields = "missing_required_fields"
    already_exist_fields = "already_exist_fields"
    bad_formatted_fields = "bad_formatted_fields"
    error_details = "error_details"
    message_key = "message"
    schema_dict = {
        'type': openapi.TYPE_OBJECT,
        'title': "Response body for status code 400",
        'description': "Following keys are returned as json",
        'properties': {
            already_exist_fields: {
                'type': FIELD_TYPES[already_exist_fields],
                'description': GENERAL_DESCRIPTIONS[already_exist_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            bad_formatted_fields: {
                'type': FIELD_TYPES[bad_formatted_fields],
                'description': GENERAL_DESCRIPTIONS[bad_formatted_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            missing_required_fields: {
                'type': FIELD_TYPES[missing_required_fields],
                'description': GENERAL_DESCRIPTIONS[missing_required_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            error_details: {
                'type': FIELD_TYPES[error_details],
                'description': GENERAL_DESCRIPTIONS[error_details],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            message_key: {
                'type': FIELD_TYPES[message_key],
                'description': GENERAL_DESCRIPTIONS[message_key],
            },
        }
    }
    return openapi.Schema(**schema_dict)


def build_response_dictionary(status_list, is_description=True):
    '''
    Builds the response dictionary from the list of tuples which will be used by
    swagger_auto_schema. The form of the tuples is:
    (status_codes_dictionary_key,resource_name,return type)
    resource_names and return type are necessary sometimes depending on the status_codes_dictionary_key

    Arguments:
        status_list (1d list): The list with correct keys according to the required format
    Raises:
        KeyNotFoundException if any key is not found in any dictionary
    '''
    response_dict = {}

    for status_item in status_list:
        code, msg = get_code_and_response(status_item, is_description)
        if code in response_dict.keys():
            response_dict[code] += ' or ' + msg
            # response_dict[code]+= ' and ' + msg
        else:
            response_dict[code] = msg

    return response_dict


def get_code_and_response(status_item,is_description=False):
    """
    Test

    Arguments:
        status_item (list): A list with size 1,2 or 3 with the appropriate keys according to
            STATUS_CODES defined in status_codes.py
            1st position of the list corresponds to the key of STATUS_CODES dict in status_codes py
            2nd position of the list corresponds to the resource_name and should be used with a key
            that starts with the prefix \'resource\'
            3rd position corresponds to another resource name which is somehow related
            with the resource_name in the 2nd position of the list
            Should be used only when 1st position of the dict is a key of the STATUS_CODES that is related with 2 resources
        is_description (bool):
            Whether the actual value of the variable should be present or the type of the variable.

    Returns:
        status_code,message according to the status_item contents

    """
    # log.info("STATUS_ITEM: {}".format(status_item))
    # log.info("STATUS_CODES.keys(): {}".format(STATUS_CODES.keys()))
    code = ''
    msg = ''

    if status_item[0] in STATUS_CODES.keys():
        if len(status_item)==1:
            msg = STATUS_CODES[status_item[0]]['msg']
        elif len(status_item)==2:
            msg = STATUS_CODES[status_item[0]]['msg'].format(RESOURCE_NAMES[status_item[1]])
        elif len(status_item)==3:
            msg = STATUS_CODES[status_item[0]]['msg'].format(RESOURCE_NAMES[status_item[1]],RESPONSE_TYPES[status_item[2]])
        code = STATUS_CODES[status_item[0]]['code']
    elif status_item[0] in VARIABLE_RESULTS.keys():
        if is_description:
            type_list = VARIABLE_RESULTS[status_item[0]]['type']
            msg = VARIABLE_RESULTS[status_item[0]]['msg']%(tuple(type_list))
        else:
            msg = VARIABLE_RESULTS[status_item[0]]['msg']%(tuple(status_item[1:]))
        code = VARIABLE_RESULTS[status_item[0]]['code']
    return code,msg


def build_fields(classname, status_keys):
    """Builds the dictionary which will be put as input to the swagger_auto_schema response.
    Keys will be of type (str) and will represent the status code and values will be of
    type rest_framework.response.Response.

    Args:
        classname (str):
            The classname of the caller
        status_keys (2d list):
            A 2d list where each sublist contains the keys specified in status_codes.STATUS_CODES & status_codes.RESOURCE_NAMES
            with their description

    Returns:
        A dict object where key is the status code and value is the openapi.Schema object
        If no keys are given in status_keys that correspond to 400 or 405 status codes then the function
        will autogenerate openapi.Schema objects for them.
    Raises:
        KeyNotFoundException if the status_keys given do not match with VIEWS_DESCRIPTION
        status codes of the given class.
    """
    status_text = build_response_dictionary(status_keys)
    response_dict = {}
    field_dict = {}
    for response_body in VIEWS_DESCRIPTION[classname]:
        property_dict = {}
        for variable_name in response_body['variables']:
            property_dict[variable_name] = {
                'type': FIELD_TYPES[variable_name],
                'description': GENERAL_DESCRIPTIONS[variable_name]
            }
            #check if there is a list of values allowed for this field
            if variable_name in ENUM_VARIABLES[classname]:
                property_dict[variable_name]['enum'] = ENUM_VARIABLES[classname][variable_name]
            if FIELD_TYPES[variable_name]==openapi.TYPE_ARRAY:
                property_dict[variable_name]['items'] = {
                    'type': openapi.TYPE_STRING
                }

        schema_dict = {
            'type': openapi.TYPE_OBJECT,
            'description': 'Following keys are returned as json'
        }

        for status_code in response_body['status_code']:
            schema_dict['title'] = 'Response body for status code {}'.format(status_code)

            #build the custom response and ignore the variable type
            if classname in CUSTOM_RESPONSES and status_code in CUSTOM_RESPONSES[classname]:
                schema_dict = CUSTOM_RESPONSES[classname][status_code]
            else:
                schema_dict['properties'] = property_dict

            response_dict[status_code] = openapi.Response(
                description=status_text[status_code],
                schema=openapi.Schema(**schema_dict)
            )

    # bad method status code
    response_dict[405] = openapi.Response(status_text[405],_wrong_method_schema())

    if classname not in IGNORE_BAD_REQUEST:
        #if no bad request case is specified, it has to be generated
        if 400 not in response_dict:
            response_dict[400] = openapi.Response(status_text[400],_bad_request_schema())

    #fill the remaining keys which do not have a documented response body with just their response text description
    for status_code in status_text.keys():
        if not status_code in response_dict.keys():
            response_dict[status_code]=status_text[status_code]

    return response_dict
