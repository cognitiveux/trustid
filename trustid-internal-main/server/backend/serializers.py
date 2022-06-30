# Serializers define the API representation.
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.fields import JSONField
from django.utils.six import text_type
from drf_yasg import openapi
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

import datetime
import jsonschema

from .application_error import ApplicationError
from .logging import logger as log
from .models import *
from .status_codes import (
    get_code_and_response,
    STATUS_CODES,
)
from .views_utils import generate_random_uuid


ALREADY_EXISTS_FIELDS = "already_exists_fields"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
ERROR_DETAILS = "error_details"
MESSAGE = "message"
MISSING_REQUIRED_FIELDS = "missing_required_fields"
UNIQUE = "unique"
DJANGO_VALIDATION_ERROR_CODES = [
    "invalid",
    "invalid_choice",
    "min_length",
    "min_value",
    "max_length",
    "max_value",
]
MY_JSON_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'exam_id': {
            'type': 'integer'
        },
        'students_emails': {
            'type': 'array'
        }
    },
    'required': ['exam_id', 'students_emails']
}

CHECKUP_PROCESS_JSON_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'array',
}


def formatted_error_response_empty_params(validation_error):
    response = {
        ALREADY_EXISTS_FIELDS: [],
        BAD_FORMATTED_FIELDS: [],
        MISSING_REQUIRED_FIELDS: []
    }
    response[MESSAGE] = validation_error.__repr__()
    return response


class CustomSerializer(serializers.ModelSerializer):
    """
    A custom class to implement a way to return any validation errors
    in the desired format
    """
    def formatted_error_response(self, include_already_exists=False):
        """
        Returns (dict):
            A dictionary with the errors when a status code 400 bad request has occured
        """
        error_details_dict = {}
        response = {
            ALREADY_EXISTS_FIELDS: [],
            BAD_FORMATTED_FIELDS: [],
            MISSING_REQUIRED_FIELDS: []
        }
        append_bad_request_msg = False

        for field in self._errors:
            if self._errors[field][0].code == UNIQUE:
                response[ALREADY_EXISTS_FIELDS].append(field)

            elif self._errors[field][0].code in DJANGO_VALIDATION_ERROR_CODES:
                response[BAD_FORMATTED_FIELDS].append(field)
            else:
                response[MISSING_REQUIRED_FIELDS].append(field)

            # Add descriptive error messages
            error_details_dict[field] = []

            for item in self._errors[field]:
                error_details_dict[field].append(item)

        if not include_already_exists:
            response.pop(ALREADY_EXISTS_FIELDS)

        response[ERROR_DETAILS] = error_details_dict

        return response


class AddExamSerializer(CustomSerializer):
    exam_type = models.CharField(max_length=7, choices=ExamTypeModel.EXAM_TYPE_CHOICES)

    class Meta:
        model = Examination
        fields = ('additional_material', 'duration', 'exam_type', 'name', 'privacy_policy', 'scheduled_date', )
        extra_kwargs = {
            'additional_material': {
                'required': False
            },
            'duration': {
                'required': True
            },
            'exam_type': {
                'required': True
            },
            'name': {
                'required': True
            },
            'privacy_policy': {
                'required': True
            },
            'scheduled_date': {
                'required': True
            },
        }


class InstructorManualApproveStudentSerializer(CustomSerializer):

    class Meta:
        model = ManualApproveStudent
        fields = ('exam_id', 'email', )
        extra_kwargs = {
            'exam_id': {
                'required': True
            },
            'email': {
                'required': True
            },
        }


class DetectLowContrastSerializer(CustomSerializer):
    class Meta:
        model = LowContrast
        fields = ('image', )
        extra_kwargs = {
            'image': {
                'required': True
            },
        }


class HeadPoseClassificationSerializer(CustomSerializer):
    class Meta:
        model = LowContrast
        fields = ('image', )
        extra_kwargs = {
            'image': {
                'required': True
            },
        }


class EnrollJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Enrollment Details",
            "properties": {
                "exam_id": openapi.Schema(
                    title="ID of examination",
                    type=openapi.TYPE_INTEGER,
                    maxLength=50,
                ),
                "students_emails": openapi.Schema(
                    title="Emails of students to enroll",
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING)
                ),
            },
            "required": ["exam_id", "students_emails"],
         }


class EnrollStudentsSerializer(CustomSerializer):
    details = EnrollJSONField()

    def custom_validate(value):
        """
        Check that the input fields are valid JSON based on the schema
        """
        try:
            jsonschema.validate(value, MY_JSON_FIELD_SCHEMA)
            return value
        except jsonschema.exceptions.ValidationError as exc:
           raise serializers.ValidationError(exc)

    class Meta:
        model = ExaminationEnrollment
        fields = ('details', )
        extra_kwargs = {
            'details': {
                'required': True
            },
        }


class InstructorListExamSerializer(CustomSerializer):
    def validate(self, data):
        """
        Check that no input fields were given
        """
        if data:
            raise serializers.ValidationError("Input parameters should not be provided")

        return data

    class Meta:
        fields = ()
        model = ExaminationStatus


class ExamConditionUpdateSerializer(CustomSerializer):
    class Meta:
        model = ExaminationConditionUpdate
        fields = ('condition', 'exam_id', )
        extra_kwargs = {
            'condition': {
                'required': True
            },
            'exam_id': {
                'required': True
            },
        }


class LoginSerializer(TokenObtainPairSerializer):
    """
    The serializer for creating a JWT
    """
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        """
        Returns:
            The generated JWT
        """
        token = super(LoginSerializer, cls).get_token(user)
        email = user.email
        user_row = Users.objects.filter(email=email).values('role', 'organization', 'name', 'surname')
        user_row_role = user_row[0].get('role')
        user_row_organization = user_row[0].get('organization')
        user_row_name = user_row[0].get('name')
        user_row_surname = user_row[0].get('surname')

        # Create custom JWT
        token['iss'] = "TrustidAuthentication"
        token['iat'] = int(str(datetime.datetime.now().timestamp()).split('.')[0])
        token['sub'] = email
        token['organization'] = user_row_organization
        token['name'] = user_row_name
        token['organization'] = user_row_organization
        token['role'] = user_row_role
        token['session_id'] = generate_random_uuid()
        token['surname'] = user_row_surname

        return token

    def validate(self, attrs):
        '''
        Validation for JSON Web Token creation.

        Returns:
            status_code, response_body
        '''
        user = None
        self.response_body = {}
        bad_formatted_fields = []
        missing_required_fields = []
        already_exists_fields = []
        error_details_dict = {}

        for field_name in self.fields:
            try:
                self.fields[field_name].run_validation(attrs.get(field_name))
            except serializers.ValidationError as e:
                # treat blank as missing field
                if e.detail[0].code == 'blank' or e.detail[0].code == 'null':
                    missing_required_fields.append(field_name)
                else:
                    bad_formatted_fields.append(field_name)

                if field_name not in error_details_dict:
                    error_details_dict[field_name] = []

                error_details_dict[field_name].append(e.__repr__())

        # Check for bad formatted fields
        if len(bad_formatted_fields) > 0 or len(missing_required_fields) > 0:
            log.debug("[LoginSerializer] [validate] Bad formatted fields")
            self.response_body[MISSING_REQUIRED_FIELDS] = missing_required_fields
            self.response_body[BAD_FORMATTED_FIELDS] = bad_formatted_fields
            self.response_body[ALREADY_EXISTS_FIELDS] = already_exists_fields
            self.response_body[ERROR_DETAILS] = error_details_dict
            status, message = get_code_and_response(['bad_request'])
            self.response_body[MESSAGE] = message
            return status, self.response_body

        email = attrs.get('email')
        password = attrs.get('password')
        user_row = Users.objects.filter(email=email).first()

        # Check if user does not exist and return appropriate error code
        if not user_row:
            log.debug("[LoginSerializer] [validate] User not found")
            raise ApplicationError(['resource_not_found', 'user'])

        if user_row.check_password(password):
            log.info("[LoginSerializer] [validate] Valid credentials")
            refresh = self.get_token(user_row)
            status_code, message = get_code_and_response(['resource_created_return_obj', 'jwt'])
            self.response_body[MESSAGE] = message
            self.response_body['resource_name'] = 'jwt'
            tokens = {
                'access': text_type(refresh.access_token),
                'refresh': text_type(refresh)
            }
            self.response_body['resource_obj'] = tokens
            return status_code, self.response_body
        else:
            log.info("[LoginSerializer] [validate] Invalid credentials")
            raise ApplicationError(['unauthorized'])

    def formatted_error_response(self):
        '''
        Returns:
            The response body produced by the validate function
        '''
        return self.response_body


class MonitoringSerializer(CustomSerializer):

    class Meta:
        model = MonitoringActivity
        fields = ('exam_id', 'image', 'running_processes', 'ip_address',)
        extra_kwargs = {
            'exam_id': {
                'required': True
            },
            'image': {
                'required': True
            },
            'running_processes': {
                'required': True
            },
            'ip_address': {
                'required': False
            },
        }


class RefreshTokenSerializer(TokenRefreshSerializer):
    """
    The serializer for refreshing a JWT
    """
    def validate(self, attrs):
        '''
        Validation for refreshing JSON Web Token.

        Returns:
            status_code, response_body
        '''
        self.response_body = {}
        bad_formatted_fields = []
        missing_required_fields = []
        already_exists_fields = []
        error_details_dict = {}

        for field_name in self.fields:
            try:
                self.fields[field_name].run_validation(attrs.get(field_name))
            except serializers.ValidationError as e:
                # treat blank as missing field
                if e.detail[0].code == 'blank' or e.detail[0].code == 'null':
                    missing_required_fields.append(field_name)
                else:
                    bad_formatted_fields.append(field_name)

                if field_name not in error_details_dict:
                    error_details_dict[field_name] = []

                error_details_dict[field_name].append(e.__repr__())

        # Check for bad formatted fields
        if len(bad_formatted_fields) > 0 or len(missing_required_fields) > 0:
            log.debug("[RefreshTokenSerializer] Bad formatted fields")
            self.response_body[MISSING_REQUIRED_FIELDS] = missing_required_fields
            self.response_body[BAD_FORMATTED_FIELDS] = bad_formatted_fields
            self.response_body[ALREADY_EXISTS_FIELDS] = already_exists_fields
            self.response_body[ERROR_DETAILS] = error_details_dict
            status,message = get_code_and_response(['bad_request'])
            self.response_body[MESSAGE] = message
            return status, self.response_body

        try:
            token = super(RefreshTokenSerializer, self).validate(attrs)
            status_code, message = get_code_and_response(['resource_created_return_str', 'jwt'])
            self.response_body[MESSAGE] = message
            self.response_body['resource_name'] = 'jwt'
            self.response_body['resource_str'] = text_type(token.get('access'))
            return status_code, self.response_body
        except Exception as e:
            log.info("[RefreshTokenSerializer] Error occurred during validation of JWT: {}".format(str(e)))
            status_code, message = get_code_and_response(['unauthorized'])
            message = str(e)
            self.response_body['message'] = message
            return status_code, self.response_body


class RegisterUserSerializer(CustomSerializer):

    class Meta:
        model = Users
        fields = ('email', 'name', 'organization', 'password', 'role', 'surname')
        extra_kwargs = {
            'email': {
                'required': True
            },
            'name': {
                'required': True
            },
            'organization': {
                'required': True
            },
            'password': {
                'required': True
            },
            'role': {
                'required': True
            },
            'surname': {
                'required': True
            },
        }


class SampleAuthenticatedSerializer(CustomSerializer):
    class Meta:
        model = Users
        fields = ()


class CheckupProcessJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_ARRAY,
            "title": "Running Processes",
            "items": openapi.Items(type=openapi.TYPE_STRING)
         }


class StudentCheckVerificationStatusSerializer(CustomSerializer):
    class Meta:
        model = RequestManualApproval
        fields = ('exam_id',)
        extra_kwargs = {
            'exam_id': {
                'required': True
            },
        }


class StudentCheckupProcessSerializer(CustomSerializer):
    running_processes = CheckupProcessJSONField()

    def custom_validate(value):
        """
        Check that the input fields are valid JSON based on the schema
        """
        try:
            jsonschema.validate(value, CHECKUP_PROCESS_JSON_FIELD_SCHEMA)
            return value
        except jsonschema.exceptions.ValidationError as exc:
           raise serializers.ValidationError(exc)

    class Meta:
        model = StudentProcesses
        fields = ('running_processes',)
        extra_kwargs = {
            'running_processes': {
                'required': True
            },
        }


class StudentSubmitFeedbackSerializer(CustomSerializer):
    cheat_mode = models.CharField(max_length=13, choices=ExamCheatModel.EXAM_CHEAT_MODE_CHOICES)

    class Meta:
        model = StudentFeedback
        fields = ('cheat_mode', 'exam_id', 'feedback', )
        extra_kwargs = {
            'cheat_mode': {
                'required': True
            },
            'exam_id': {
                'required': True
            },
            'feedback': {
                'required': True
            },
        }


class StudentIdentificationSerializer(CustomSerializer):
    class Meta:
        model = StudentIdentification
        fields = ('exam_id', 'image',)
        extra_kwargs = {
            'exam_id': {
                'required': True
            },
            'image': {
                'required': True
            },
        }


class StudentRequestManualApprovalSerializer(CustomSerializer):
    class Meta:
        model = RequestManualApproval
        fields = ('exam_id',)
        extra_kwargs = {
            'exam_id': {
                'required': True
            },
        }


class StudentListExamSerializer(CustomSerializer):
    def validate(self, data):
        """
        Check that no input fields were given
        """
        if data:
            raise serializers.ValidationError("Input parameters should not be provided")

        return data

    class Meta:
        fields = ()
        model = ExaminationStatus


class TrustidVersionSerializer(CustomSerializer):
    def validate(self, data):
        """
        Check that no input fields were given
        """
        if data:
            raise serializers.ValidationError("Input parameters should not be provided")

        return data

    class Meta:
        fields = ()
        model = Users


class UpdateExamSerializer(CustomSerializer):
    exam_type = models.CharField(max_length=7, choices=ExamTypeModel.EXAM_TYPE_CHOICES)

    class Meta:
        model = Examination
        fields = ('additional_material', 'duration', 'exam_id', 'exam_type', 'privacy_policy', 'scheduled_date', )
        extra_kwargs = {
            'additional_material': {
                'required': False
            },
            'duration': {
                'required': True
            },
            'exam_id': {
                'required': True,
                'validators': []
            },
            'exam_type': {
                'required': True
            },
            'privacy_policy': {
                'required': True
            },
            'scheduled_date': {
                'required': True
            },
        }
