from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template import loader
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (
    permissions,
    serializers as rf_serializers,
    status,
)
from rest_framework.exceptions import ParseError
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import base64
import cv2
import io
from imageio import imread
import joblib
import json
import jwt
import numpy as np
import time
import zlib

from trustid_project.celery import (
    app,
)
from .application_error import ApplicationError

from .logging import logger as log
from .models import *
#from .rFaceID import (
#    FaceDetectionResultValueEnum,
#    FaceRecognitionResultValueEnum,
#    ImageQualityResultValueEnum,
#    PoseEstimationResultValueEnum,
#)
from .rFaceID import *
from .serializers import *
from .status_codes import *
from .views_utils import *


BAD_REQUEST = "bad_request"
CONTENT = "content"
INTERNAL_SERVER_ERROR = "internal_server_error"
STRING_TYPE = "_str"
DICT_TYPE = "_dict"
ARRAY_TYPE = "_array"
BOOLEAN_TYPE = "_bool"
MESSAGE = "message"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
MISSING_REQUIRED_FIELDS = "missing_required_fields"
METHOD_NOT_ALLOWED = "method_not_allowed"
STATUS_CODE = "status_code"
RESOURCE = "resource"
RESOURCE_NAME = "resource_name"

ALREADY_EXISTS_FIELDS = "already_exists_fields"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
ERROR_DETAILS = "error_details"
MISSING_REQUIRED_FIELDS = "missing_required_fields"


class AddExam(GenericAPIView):
    """
    post:
    The view that allows instructors to add examinations
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddExamSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AddExam', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def add_exam_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = AddExamSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                if role != RoleModel.INSTRUCTOR:
                    raise ApplicationError(['resource_not_allowed'])

                additional_material = data.get('additional_material')
                duration = data.get('duration')
                exam_id = int(str(user_id) + str(int(time.time())))
                exam_type = data.get('exam_type')
                name = data.get('name')
                instructor_id = user_id
                privacy_policy = data.get('privacy_policy')
                scheduled_date = data.get('scheduled_date')
                ts_updated = now()

                examination = Examination(
                    additional_material=additional_material,
                    duration=duration,
                    exam_id=exam_id,
                    exam_type=exam_type,
                    instructor_id=instructor_id,
                    name=name,
                    privacy_policy=privacy_policy,
                    scheduled_date=scheduled_date,
                    ts_updated=ts_updated
                )
                examination.save()

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'examination'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.add_exam_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class EnrollStudents(GenericAPIView):
    """
    post:
    The view that allows instructors to enroll students to the examinations
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EnrollStudentsSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'examination'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('EnrollStudents', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def enroll_students_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = EnrollStudentsSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                details = data.get('details')

                # JSON validation
                validated_data = EnrollStudentsSerializer.custom_validate(details)

                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )

                instructor_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                if role != RoleModel.INSTRUCTOR:
                    raise ApplicationError(['resource_not_allowed'])

                exam_id = details.get('exam_id')
                students_emails = details.get('students_emails')

                exam_exists = Examination.objects.filter(instructor_id=instructor_id, exam_id=exam_id).first()

                if not exam_exists:
                    raise ApplicationError(['resource_not_found', 'examination'])

                for student_email in students_emails:
                    student_exists = Users.objects.filter(
                        email=student_email,
                        role=RoleModel.STUDENT
                    ).first()

                    if not student_exists:
                        raise ApplicationError(['resource_not_found', 'user'])

                ts_enrolled = now()

                for student_email in students_emails:
                    student_id_row = Users.objects.filter(email=student_email).values('id')
                    student_id = student_id_row[0].get('id')

                    ExaminationStatus.objects.update_or_create(
                        exam_id=exam_id,
                        student_id=student_id,
                        defaults={
                            'instructor_id': instructor_id,
                            'status': ExamStatusModel.UPCOMING,
                            'ts_enrolled': ts_enrolled,
                        }
                    )

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'enrollment'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except rf_serializers.ValidationError as e:
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        e
                    )
                )
                response = {}
                content = {
                    ALREADY_EXISTS_FIELDS: [],
                    BAD_FORMATTED_FIELDS: [],
                    MISSING_REQUIRED_FIELDS: [],
                    MESSAGE: e.__repr__()
                }
                response[CONTENT] = content
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.enroll_students_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class InstructorListExam(GenericAPIView):
    """
    get:
    Returns the details of examinations created by the instructor
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = InstructorListExamSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('InstructorListExam', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def instructor_list_exam_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            serialized_data = InstructorListExamSerializer(data=data).validate(data)
            encoded_jwt = None
            current_jwt = request.get('META').get('HTTP_AUTHORIZATION')

            if current_jwt:
                encoded_jwt = current_jwt.split('Bearer ')[1]
            else:
                raise ApplicationError(['resource_not_found', 'user'])

            decoded_jwt = jwt.decode(
                encoded_jwt,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                audience=settings.SIMPLE_JWT['AUDIENCE']
            )
            instructor_id = decoded_jwt['user_id']

            exam_rows = Examination.objects.filter(
                instructor_id=instructor_id,
            ).values('additional_material', 'duration', 'exam_id', 'exam_type', 'name', 'privacy_policy', 'scheduled_date')

            list_of_exams = []
            enrolled_students = []
            exam_obj = {}

            for item in exam_rows:
                exam_obj = {}
                enrolled_students = []
                additional_material = item.get('additional_material')
                duration = item.get('duration')
                exam_id = item.get('exam_id')
                exam_type = item.get('exam_type')
                name = item.get('name')
                privacy_policy = item.get('privacy_policy')
                scheduled_date = item.get('scheduled_date').strftime('%Y-%m-%dT%H:%M:%S')

                exam_status_rows = ExaminationStatus.objects.filter(
                    exam_id=exam_id,
                    instructor_id=instructor_id,
                    ts_enrolled__isnull=False,
                ).values('student_id', 'status')

                status = ExamStatusModel.UPCOMING
                if exam_status_rows:
                    status = exam_status_rows[0].get('status')

                enroll_student_obj = {}

                for exam_status_row in exam_status_rows:
                    student_id = exam_status_row.get('student_id')
                    student_row = Users.objects.filter(id=student_id).values('email', 'name', 'surname',)
                    verification_status = ExaminationStatus.objects.filter(
                        student_id=student_id,
                        exam_id=exam_id,
                    ).values('verification_status')

                    if student_row:
                        user_alerts = []
                        monitoring_row = MonitoringActivity.objects.filter(
                            user_fk_id=student_id,
                            exam_id=exam_id,
                            monitoring_type=MonitoringTypeModel.EXAM_MONITORING
                        ).values('student_alerts')

                        if monitoring_row:
                            user_alerts = monitoring_row[0].get('student_alerts')
                            if not user_alerts:
                                user_alerts = []
                            else:
                                user_alerts = json.loads(user_alerts)

                        enroll_student_obj = {}
                        enroll_student_obj['email'] = student_row[0].get('email')
                        enroll_student_obj['name'] = student_row[0].get('name')
                        enroll_student_obj['surname'] = student_row[0].get('surname')
                        enroll_student_obj['verification_status'] = verification_status[0].get('verification_status')

                        final_alerts = []

                        for user_alert in user_alerts:
                            alert_obj = {}
                            alert_obj['text'] = user_alert
                            alert_obj['timestamp'] = now()
                            final_alerts.append(alert_obj)

                        enroll_student_obj['alerts'] = final_alerts
                        enrolled_students.append(enroll_student_obj)

                exam_obj['additional_material'] = additional_material
                exam_obj['duration'] = duration
                exam_obj['exam_id'] = exam_id
                exam_obj['exam_type'] = exam_type
                exam_obj['name'] = name
                exam_obj['status'] = status
                exam_obj['privacy_policy'] = privacy_policy
                exam_obj['scheduled_date'] = scheduled_date
                exam_obj['enrolled_students'] = enrolled_students

                list_of_exams.append(exam_obj)

            status_code, message = get_code_and_response(['success'])
            content = {}
            content[MESSAGE] = message
            content[RESOURCE + ARRAY_TYPE] = list_of_exams
            content[RESOURCE_NAME] = 'examination'
            response = {}
            response[CONTENT] = content
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except rf_serializers.ValidationError as e:
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    formatted_error_response_empty_params(e)
                )
            )
            response = {}
            response[CONTENT] = formatted_error_response_empty_params(e)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ],
    )
    def get(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.instructor_list_exam_task.delay(request.GET, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class InstructorManualApproveStudent(GenericAPIView):
    """
    post:
    The view that allows instructors to manually approve students.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InstructorManualApproveStudentSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['resource_not_found', 'examination'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('InstructorManualApproveStudent', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def instructor_manual_approve_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = InstructorManualApproveStudentSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                if role != RoleModel.INSTRUCTOR:
                    raise ApplicationError(['resource_not_allowed'])

                student_email = data.get('email')
                exam_id = data.get('exam_id')

                # Check if student email exists
                user_row = Users.objects.filter(email=student_email).values('id')

                if not user_row:
                    raise ApplicationError(['resource_not_found', 'user'])

                student_id = user_row[0].get('id')

                # Check if exam_id exists
                exam_id_row = ExaminationStatus.objects.filter(
                    exam_id=exam_id,
                    student_id=student_id
                )

                if not exam_id_row:
                    raise ApplicationError(['resource_not_found', 'examination'])

                exam_status_row = ExaminationStatus.objects.filter(
                    exam_id=exam_id,
                    student_id=student_id,
                ).update(
                    verification_status=VerificationStatusModel.VERIFIED,
                    ts_verified=now(),
                )

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'examination'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.instructor_manual_approve_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class Login(TokenObtainPairView):
    """
    post: Creates a JSON Web Token if the provided credentials are correct
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_created_return_obj', 'jwt'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('Login', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def login_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        log.debug("{} Requested login email: {}".format(request_details(request), data.get('email')))
        try:
            status_code, tokens = LoginSerializer(data).validate(data)
            response[CONTENT] = tokens
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.login_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class Monitoring(GenericAPIView):
    """
    post:
    The view that handles the monitoring of the running processes on the student's device
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MonitoringSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('Monitoring', response_types)

    def face_recognition(image, request):
        # define face recg threshold (only accept identities whose score is higher than fr_threshold)
        fr_threshold = 0.5          # requires tunning

        im_bytes = base64.b64decode(image)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # mirror image (horizontally)
        image = cv2.flip(image, 1)

        # convert BGR to RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # -----------------------------------------------
        # Face detection + recognition
        # -----------------------------------------------

        # run face detection (single rectangle region)
        face = rFaceID()
        face.load("models/facenet-svm-poc1-all.pth")
        detectionResult = face.detection(image)

        identity = ''
        predicted_label = ''
        confidence_score = 0.0

        detection_result = detectionResult.getResult()
        log.debug("{} Detection result: {}".format(request_details(request), detection_result))
        is_face_detected = True

        if (detection_result == FaceDetectionResultValueEnum.NO_RESULTS):
            is_face_detected = False

        # if valid detection
        if (detection_result == FaceDetectionResultValueEnum.ONE_RESULT):
            rect = detectionResult.getBoundingBox()
            # apply face recognition (CNN inference)
            result = face.recognition(imageRGB, rect, fr_threshold)
            predicted_label = result.getMatchedIdentity()
            confidence_score = result.getMatchConfidence()
            face_result = result.getResult()

            log.debug("{} face result: {}, predicted_label: {}, score: {}, debug_info: {}".format(request_details(request), face_result, predicted_label, confidence_score, result._debug_info))

            if face_result == FaceRecognitionResultValueEnum.FOUND_MATCH:
                identity = predicted_label

        return identity, predicted_label, confidence_score, is_face_detected

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def monitoring_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = MonitoringSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                running_processes = data.get('running_processes')
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                session_id = decoded_jwt['session_id']

                exam_id = data.get('exam_id')
                img_data_rcv = data.get('image')
                ip_address = data.get('ip_address')
                identified_student, predicted_label, confidence_score, is_face_detected = Monitoring.face_recognition(img_data_rcv, request)
                log.info("{} identified_student: {}".format(request_details(request), identified_student))
                img_to_store = ""
                alerts = []

                if not identified_student:
                    identified_student = ''
                    log.info("{} Face recognition did not identify any student. Will store image.".format(request_details(request)))
                    img_to_store = img_data_rcv
                else:

                    user_row = Users.objects.filter(
                        email=identified_student
                    ).values('name', 'surname',)

                    if not user_row:
                        identified_student = ''
                    else:
                        name = user_row[0].get('name')
                        surname = user_row[0].get('surname')
                        identified_student = name + " " + surname

                        legitimate_user_email = Users.objects.filter(
                            id=user_id
                        ).values('email')

                        if legitimate_user_email != identified_student:
                            alerts.append("Impersonation detected")

                not_allowed_apps = []

                for rp in running_processes:
                    if rp in settings.NOT_ALLOWED_APPS:
                        not_allowed_apps.append(rp)

                if not_allowed_apps:
                    alerts.append("Opened forbidden application")

                monitoring_activity = MonitoringActivity(
                    user_fk_id=user_id,
                    student_alerts=json.dumps(alerts),
                    predicted_label=predicted_label,
                    confidence_score=confidence_score,
                    exam_id=exam_id,
                    session_id=session_id,
                    image=img_to_store,
                    ip_address=ip_address,
                    running_processes=json.dumps(running_processes),
                    not_allowed_apps=json.dumps(not_allowed_apps),
                    identified_student=identified_student,
                    monitoring_type=MonitoringTypeModel.EXAM_MONITORING,
                    is_face_detected=is_face_detected,
                    ts_added=now()
                )
                monitoring_activity.save()

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'user'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.monitoring_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class RefreshToken(TokenRefreshView):
    """
    post: Uses the longer-lived refresh token to obtain another access token
    """
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['resource_created_return_str', 'jwt'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('RefreshToken', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def refresh_token_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            status_code, token = RefreshTokenSerializer(data).validate(data)
            response[CONTENT] = token
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.refresh_token_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class RegisterUser(CreateAPIView):
    """
    post:
    Creates a new Trustid user instance
    """
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('RegisterUser', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def register_user_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = RegisterUserSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                email = data.get('email')
                name = data.get('name')
                organization = data.get('organization')
                password = data.get('password')
                role = data.get('role')
                surname = data.get('surname')

                password_hash = make_password(password)

                user = Users(
                    email=email,
                    name=name,
                    organization=organization,
                    password=password_hash,
                    role=role,
                    surname=surname,
                    ts_registration=now()
                )
                user.save()

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'user'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.register_user_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class ExamConditionUpdate(GenericAPIView):
    """
    post:
    The view that allows instructors to start an examination
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExamConditionUpdateSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'examination'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('ExamConditionUpdate', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def exam_condition_update_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_data = ExamConditionUpdateSerializer(data=data)

        if not serialized_data.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_data.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_data.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                exam_id = data.get('exam_id')
                condition = data.get('condition')

                # Student can join or leave the exam
                if role == RoleModel.STUDENT:
                    if condition == ExamConditionModel.START:
                        raise ApplicationError(['resource_not_allowed'])
                    else:
                        exam_id_row = ExaminationStatus.objects.filter(
                            exam_id=exam_id,
                            student_id=user_id
                        )

                        if not exam_id_row:
                            raise ApplicationError(['resource_not_found', 'examination'])

                        if condition == ExamConditionModel.JOIN:
                            log.debug("{} Student: {} joining exam: {}".format(request_details(request), user_id, exam_id))
                            exam_status_row = ExaminationStatus.objects.filter(
                                exam_id=exam_id,
                                student_id=user_id,
                            ).update(
                                ts_joined=now()
                            )
                        elif condition == ExamConditionModel.LEAVE:
                            log.debug("{} Student: {} leaving exam: {}".format(request_details(request), user_id, exam_id))
                            exam_status_row = ExaminationStatus.objects.filter(
                                exam_id=exam_id,
                                student_id=user_id,
                            ).update(
                                ts_quit=now()
                            )
                elif role == RoleModel.INSTRUCTOR:
                    if condition == ExamConditionModel.JOIN or condition == ExamConditionModel.LEAVE:
                        raise ApplicationError(['resource_not_allowed'])
                    else:
                        exam_id_row = ExaminationStatus.objects.filter(
                            exam_id=exam_id,
                            instructor_id=user_id
                        )

                        if not exam_id_row:
                            raise ApplicationError(['resource_not_found', 'examination'])

                        log.debug("{} instructor: {} starting exam: {}".format(request_details(request), user_id, exam_id))
                        exam_status_row = ExaminationStatus.objects.filter(
                            exam_id=exam_id,
                            instructor_id=user_id,
                        ).update(
                            ts_started=now()
                        )

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'examination'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.exam_condition_update_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentRequestManualApproval(GenericAPIView):
    """
    post:
    Allows the student to request from the instructor to manually approve their identity for the given exam ID.
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentRequestManualApprovalSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['resource_not_found', 'examination'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentRequestManualApproval', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_request_manual_approval_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            serialized_data = StudentRequestManualApprovalSerializer(data=data).validate(data)
            encoded_jwt = None
            current_jwt = request.get('META').get('HTTP_AUTHORIZATION')

            if current_jwt:
                encoded_jwt = current_jwt.split('Bearer ')[1]
            else:
                raise ApplicationError(['resource_not_found', 'user'])

            decoded_jwt = jwt.decode(
                encoded_jwt,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                audience=settings.SIMPLE_JWT['AUDIENCE']
            )
            student_id = decoded_jwt['user_id']
            exam_id = data.get('exam_id')

            exam_id_row = ExaminationStatus.objects.filter(
                exam_id=exam_id,
                student_id=student_id
            )

            if not exam_id_row:
                raise ApplicationError(['resource_not_found', 'examination'])

            exam_status_row = ExaminationStatus.objects.filter(
                exam_id=exam_id,
                student_id=student_id,
            ).update(
                is_manual_verification=True,
                verification_status=VerificationStatusModel.REQUESTED_MANUAL_APPROVAL,
            )

            status_code, message = get_code_and_response(['success'])
            content = {}
            content[MESSAGE] = message
            content[RESOURCE_NAME] = 'user'
            response = {}
            response[CONTENT] = content
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except rf_serializers.ValidationError as e:
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    formatted_error_response_empty_params(e)
                )
            )
            response = {}
            response[CONTENT] = formatted_error_response_empty_params(e)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ],
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.student_request_manual_approval_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentCheckVerificationStatus(GenericAPIView):
    """
    post:
    The view that allows students to poll for their verification status.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentCheckVerificationStatusSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['resource_not_found', 'examination'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentCheckVerificationStatus', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_check_verification_status_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = StudentCheckVerificationStatusSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                if role != RoleModel.STUDENT:
                    raise ApplicationError(['resource_not_allowed'])

                exam_id = data.get('exam_id')

                # Check if exam_id exists
                exam_id_row = ExaminationStatus.objects.filter(
                    exam_id=exam_id,
                    student_id=user_id
                ).values('verification_status')

                if not exam_id_row:
                    raise ApplicationError(['resource_not_found', 'examination'])

                verification_status = exam_id_row[0].get('verification_status')
                is_verified = False

                if verification_status == VerificationStatusModel.VERIFIED:
                    is_verified = True

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'user'
                content[RESOURCE + BOOLEAN_TYPE] = is_verified
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.student_check_verification_status_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentCheckupProcess(GenericAPIView):
    """
    post:
    Returns the list of processes that are not allowed to run in the student's device
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentCheckupProcessSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentCheckupProcess', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_checkup_process_task(self, data, request):
        log.debug("{} START".format(request_details(request)))
        serialized_data = StudentCheckupProcessSerializer(data=data)

        if not serialized_data.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_data.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_data.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                running_processes = data.get('running_processes')

                # JSON validation
                validated_data = StudentCheckupProcessSerializer.custom_validate(running_processes)

                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                session_id = decoded_jwt['session_id']
                not_allowed_apps = []

                for rp in running_processes:
                    if rp in settings.NOT_ALLOWED_APPS:
                        not_allowed_apps.append(rp)

                monitoring_activity = MonitoringActivity(
                    user_fk_id=user_id,
                    session_id=session_id,
                    running_processes=json.dumps(running_processes),
                    not_allowed_apps=json.dumps(not_allowed_apps),
                    monitoring_type=MonitoringTypeModel.CHECKUP_PROCESS,
                    ts_added=now()
                )
                monitoring_activity.save()

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'process'
                content[RESOURCE + ARRAY_TYPE] = not_allowed_apps
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except rf_serializers.ValidationError as e:
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        e
                    )
                )
                response = {}
                content = {
                    ALREADY_EXISTS_FIELDS: [],
                    BAD_FORMATTED_FIELDS: [],
                    MISSING_REQUIRED_FIELDS: [],
                    MESSAGE: e.__repr__()
                }
                response[CONTENT] = content
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ],
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.student_checkup_process_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentIdentification(GenericAPIView):
    """
    post:
    Returns the details of the student identified based on the image received
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentIdentificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentIdentification', response_types)

    def face_recognition(image, request):
        # define face recg threshold (only accept identities whose score is higher than fr_threshold)
        fr_threshold = 0.5          # requires tunning

        im_bytes = base64.b64decode(image)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        # mirror image (horizontally)
        image = cv2.flip(image, 1)

        # convert BGR to RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # -----------------------------------------------
        # Face detection + recognition
        # -----------------------------------------------

        # run face detection (single rectangle region)
        face = rFaceID()
        face.load("models/facenet-svm-poc1-all.pth")
        detectionResult = face.detection(image)

        identity = ''
        predicted_label = ''
        confidence_score = 0.0

        detection_result = detectionResult.getResult()
        log.debug("{} Detection result: {}".format(request_details(request), detection_result))
        is_face_detected = True

        if (detection_result == FaceDetectionResultValueEnum.NO_RESULTS):
            is_face_detected = False

        # if valid detection
        if (detection_result == FaceDetectionResultValueEnum.ONE_RESULT):
            rect = detectionResult.getBoundingBox()
            # apply face recognition (CNN inference)
            result = face.recognition(imageRGB, rect, fr_threshold)
            predicted_label = result.getMatchedIdentity()
            confidence_score = result.getMatchConfidence()
            face_result = result.getResult()

            log.debug("{} face result: {}, predicted_label: {}, score: {}, debug_info: {}".format(request_details(request), face_result, predicted_label, confidence_score, result._debug_info))

            if face_result == FaceRecognitionResultValueEnum.FOUND_MATCH:
                identity = predicted_label

        return identity, predicted_label, confidence_score, is_face_detected

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_identification_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            serialized_data = StudentIdentificationSerializer(data=data).validate(data)
            encoded_jwt = None
            current_jwt = request.get('META').get('HTTP_AUTHORIZATION')

            if current_jwt:
                encoded_jwt = current_jwt.split('Bearer ')[1]
            else:
                raise ApplicationError(['resource_not_found', 'user'])

            decoded_jwt = jwt.decode(
                encoded_jwt,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                audience=settings.SIMPLE_JWT['AUDIENCE']
            )
            student_id = decoded_jwt['user_id']
            session_id = decoded_jwt['session_id']

            img_data_rcv = data.get('image')
            exam_id = data.get('exam_id')
            img_to_store = ""

            identified_student, predicted_label, confidence_score, is_face_detected = StudentIdentification.face_recognition(img_data_rcv, request)
            log.info("{} identified_student: {}, predicted_label: {}, confidence_score: {}, is_face_detected: {}".format(request_details(request), identified_student, predicted_label, confidence_score, is_face_detected))

            # Check if the identified student matches the current student id from the jwt
            if not identified_student:
                identified_student = ''
                log.info("{} Face recognition did not identify any student. Will store image.".format(request_details(request)))
                img_to_store = img_data_rcv
            else:
                user_row = Users.objects.filter(
                    id=student_id
                ).values('email', 'name', 'surname',)

                name = user_row[0].get('name')
                surname = user_row[0].get('surname')
                email = user_row[0].get('email')

                if email != identified_student:
                    identified_student = ''
                else:
                    log.debug("Will update examination status. student id: {}, exam_id: {}".format(student_id, exam_id))
                    identified_student = name + " " + surname
                    exam_status_row = ExaminationStatus.objects.filter(
                        exam_id=exam_id,
                        student_id=student_id,
                    ).update(
                        is_manual_verification=False,
                        verification_status=VerificationStatusModel.VERIFIED,
                        ts_verified=now(),
                    )
            
            monitoring_activity = MonitoringActivity(
                user_fk_id=student_id,
                exam_id=exam_id,
                session_id=session_id,
                image=img_to_store,
                identified_student=identified_student,
                monitoring_type=MonitoringTypeModel.IDENTIFICATION,
                predicted_label=predicted_label,
                confidence_score=confidence_score,
                is_face_detected=is_face_detected,
                ts_added=now()
            )
            monitoring_activity.save()

            status_code, message = get_code_and_response(['success'])
            content = {}
            content[MESSAGE] = message
            content[RESOURCE + STRING_TYPE] = identified_student
            content[RESOURCE_NAME] = 'user'
            response = {}
            response[CONTENT] = content
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except rf_serializers.ValidationError as e:
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    formatted_error_response_empty_params(e)
                )
            )
            response = {}
            response[CONTENT] = formatted_error_response_empty_params(e)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ],
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.student_identification_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentListExam(GenericAPIView):
    """
    get:
    Returns the details of the examinations in which the student has been enrolled
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentListExamSerializer
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentListExam', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_list_exam_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            serialized_data = StudentListExamSerializer(data=data).validate(data)
            encoded_jwt = None
            current_jwt = request.get('META').get('HTTP_AUTHORIZATION')

            if current_jwt:
                encoded_jwt = current_jwt.split('Bearer ')[1]
            else:
                raise ApplicationError(['resource_not_found', 'user'])

            decoded_jwt = jwt.decode(
                encoded_jwt,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                audience=settings.SIMPLE_JWT['AUDIENCE']
            )
            student_id = decoded_jwt['user_id']
            role = decoded_jwt['role']

            if role != RoleModel.STUDENT:
                raise ApplicationError(['resource_not_allowed'])

            exam_status_rows = ExaminationStatus.objects.filter(
                student_id=student_id,
                ts_enrolled__isnull=False,
            ).values('exam_id', 'status')

            list_of_exams = []
            exam_obj = {}

            for item in exam_status_rows:
                exam_obj = {}
                exam_id = item.get('exam_id')
                status = item.get('status')

                exam_row = Examination.objects.filter(
                    exam_id=exam_id
                ).values('name', 'privacy_policy', 'scheduled_date', 'additional_material', 'duration', 'exam_type')

                name = exam_row[0].get('name')
                privacy_policy = exam_row[0].get('privacy_policy')
                scheduled_date = exam_row[0].get('scheduled_date')
                additional_material = exam_row[0].get('additional_material')
                duration = exam_row[0].get('duration')
                exam_type = exam_row[0].get('exam_type')

                exam_obj['exam_id'] = exam_id
                exam_obj['name'] = name
                exam_obj['status'] = status
                exam_obj['scheduled_date'] = scheduled_date.strftime('%Y-%m-%dT%H:%M:%S')
                exam_obj['privacy_policy'] = privacy_policy
                exam_obj['additional_material'] = additional_material
                exam_obj['duration'] = duration
                exam_obj['exam_type'] = exam_type
                list_of_exams.append(exam_obj)

            status_code, message = get_code_and_response(['success'])
            content = {}
            content[MESSAGE] = message
            content[RESOURCE + ARRAY_TYPE] = list_of_exams
            content[RESOURCE_NAME] = 'examination'
            response = {}
            response[CONTENT] = content
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except rf_serializers.ValidationError as e:
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    formatted_error_response_empty_params(e)
                )
            )
            response = {}
            response[CONTENT] = formatted_error_response_empty_params(e)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ],
    )
    def get(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.student_list_exam_task.delay(request.GET, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class StudentSubmitFeedback(GenericAPIView):
    """
    post:
    The view that handles the monitoring of the running processes on the student's device
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentSubmitFeedbackSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_found', 'examination'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('StudentSubmitFeedback', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def student_submit_feedback_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_user = StudentSubmitFeedbackSerializer(data=data)

        if not serialized_user.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_user.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_user.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                session_id = decoded_jwt['session_id']
                feedback = data.get('feedback')
                cheat_mode = data.get('cheat_mode')
                exam_id = data.get('exam_id')

                exam_exists = ExaminationStatus.objects.filter(student_id=user_id, exam_id=exam_id).first()

                if not exam_exists:
                    raise ApplicationError(['resource_not_found', 'examination'])

                student_feedback = StudentFeedback(
                    user_fk_id=user_id,
                    exam_id=exam_id,
                    session_id=session_id,
                    feedback=feedback,
                    cheat_mode=cheat_mode,
                    ts_added=now()
                )
                student_feedback.save()

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'user'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.student_submit_feedback_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class TrustidVersion(GenericAPIView):
    """
    get:
    Returns the versions of Trustid applications
    """
    serializer_class = TrustidVersionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def trustid_version_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        try:
            serialized_data = TrustidVersionSerializer(data=data).validate(data)
            status_code, message = get_code_and_response(['success'])
            content = {}
            content[MESSAGE] = message
            content[RESOURCE + DICT_TYPE] = {
                'server_version': settings.SERVER_VERSION,
                'windows_version': settings.WINDOWS_VERSION,
                'macos_version': settings.MACOS_VERSION,
                'timestamp': now().timestamp()
            }
            content[RESOURCE_NAME] = 'version'
            response = {}
            response[CONTENT] = content
            response[STATUS_CODE] = status_code
            log.debug("{} SUCCESS".format(request_details(request)))
            return response
        except rf_serializers.ValidationError as e:
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    formatted_error_response_empty_params(e)
                )
            )
            response = {}
            response[CONTENT] = formatted_error_response_empty_params(e)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        except ApplicationError as e:
            log.info("{} ERROR: {}".format(request_details(request), str(e)))
            response = {}
            response[CONTENT] = e.get_response_body()
            response[STATUS_CODE] = e.status_code
            return response

    @swagger_auto_schema(
        responses=build_fields('TrustidVersion', response_types),
        security=[]
    )
    def get(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            result = self.trustid_version_task.delay(request.GET, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class UpdateExamDetails(GenericAPIView):
    """
    post:
    The view that allows instructors to update the details of examinations
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateExamSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['resource_not_found', 'examination'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('UpdateExamDetails', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def update_exam_details_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_data = UpdateExamSerializer(data=data)

        if not serialized_data.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_data.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_data.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                current_jwt = request.get('META').get('HTTP_AUTHORIZATION')
                encoded_jwt = None

                if current_jwt:
                    encoded_jwt = current_jwt.split('Bearer ')[1]
                else:
                    raise ApplicationError(['resource_not_found', 'user'])

                decoded_jwt = jwt.decode(
                    encoded_jwt,
                    settings.SIMPLE_JWT['SIGNING_KEY'],
                    settings.SIMPLE_JWT['ALGORITHM'],
                    audience=settings.SIMPLE_JWT['AUDIENCE']
                )
                user_id = decoded_jwt['user_id']
                role = decoded_jwt['role']

                if role != RoleModel.INSTRUCTOR:
                    raise ApplicationError(['resource_not_allowed'])

                exam_id = data.get('exam_id')
                exam_exists = Examination.objects.filter(instructor_id=user_id, exam_id=exam_id).first()

                if not exam_exists:
                    raise ApplicationError(['resource_not_found', 'examination'])

                additional_material = data.get('additional_material')
                duration = data.get('duration')
                exam_type = data.get('exam_type')
                instructor_id = user_id
                privacy_policy = data.get('privacy_policy')
                scheduled_date = data.get('scheduled_date')
                ts_updated = now()

                Examination.objects.filter(
                    exam_id=exam_id,
                    instructor_id=instructor_id,
                ).update(
                    additional_material=additional_material,
                    duration=duration,
                    exam_type=exam_type,
                    privacy_policy=privacy_policy,
                    scheduled_date=scheduled_date,
                    ts_updated=ts_updated
                )

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'examination'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.update_exam_details_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])



class DetectLowContrast(GenericAPIView):
    """
    post:
    The view that detects whether the image contrast is low or not
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.AllowAny,)
    serializer_class = DetectLowContrastSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('DetectLowContrast', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def detect_low_contrast_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_data = DetectLowContrastSerializer(data=data)

        if not serialized_data.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_data.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_data.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                image = data.get('image')
                im_bytes = base64.b64decode(image)
                im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
                image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

                # mirror image (horizontally)
                image = cv2.flip(image, 1)

                # convert BGR to RGB
                imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # run face detection (single rectangle region)
                detectionResult = settings.ML_FACE_REC.detection(imageRGB)

                extra_details = ''
                is_incorrect_contrast = False

                if (detectionResult.getResult() == FaceDetectionResultValueEnum.ONE_RESULT):
                    log.debug("ONE_RESULT detected.")

                    # draw detection rectangle
                    rect = detectionResult.getBoundingBox()

                    # image quality check
                    result = settings.ML_FACE_REC.checkImageQuality(image, rect)

                    if (result.getResult() == ImageQualityResultValueEnum.VERY_LOW_ILUMINATION):
                        log.debug("VERY_LOW_ILUMINATION")
                        extra_details = "Low light conditions detected. Please adjust your light conditions and retry."
                        is_incorrect_contrast = True
                    elif (result.getResult() == ImageQualityResultValueEnum.VERY_HIGH_ILUMINATION):
                        log.debug("VERY_HIGH_ILUMINATION")
                        extra_details = "High light conditions detected. Please adjust your light conditions and retry."
                        is_incorrect_contrast = True
                    else:
                        log.debug("GOOD IMAGE CONTRAST")

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'image'
                content[RESOURCE + BOOLEAN_TYPE] = is_incorrect_contrast
                content['extra_details'] = extra_details
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.detect_low_contrast_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class HeadPoseClassification(GenericAPIView):
    """
    post:
    The view that classifies the head pose of the individual based on the provided image
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.AllowAny,)
    serializer_class = HeadPoseClassificationSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('HeadPoseClassification', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def head_pose_classification_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_data = HeadPoseClassificationSerializer(data=data)

        if not serialized_data.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_data.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_data.formatted_error_response(include_already_exists=True)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                image = data.get('image')
                im_bytes = base64.b64decode(image)
                im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
                image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

                # Load head pose model
                settings.ML_FACE_REC.load_head_pose_model()

                # mirror image (horizontally)
                image = cv2.flip(image, 1)

                # convert BGR to RGB
                imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # run face detection
                detectionResult = settings.ML_FACE_REC.detection(imageRGB)

                head_pose = ''

                # if valid single detection
                if (detectionResult.getResult() == FaceDetectionResultValueEnum.ONE_RESULT):
                    rect = detectionResult.getBoundingBox()

                    # 3D head pose estimation
                    poseEstimationResult = settings.ML_FACE_REC.estimate_head_pose(imageRGB, rect)

                    # if available pose data
                    if(poseEstimationResult.getResult() == PoseEstimationResultValueEnum.SUCCESS):

                        # -> convert to pose angles from radians to degrees
                        alpha = np.rad2deg( poseEstimationResult.getPoseVector()[0] )
                        beta = np.rad2deg( poseEstimationResult.getPoseVector()[1] )
                        gamma = np.rad2deg( poseEstimationResult.getPoseVector()[2] ) - 180         # get the solution in the 1st quadrant

                        head_pose = poseEstimationResult.classifyPose()

                        log.debug("classified head pose: {}".format(head_pose))

                if head_pose:
                    head_pose = head_pose.name

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'image'
                content[RESOURCE + STRING_TYPE] = str(head_pose)
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.head_pose_classification_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
