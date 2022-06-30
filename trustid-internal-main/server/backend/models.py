from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import (
	BaseValidator,
	MinValueValidator,
)
from django.db import models
from django.utils.timezone import now


class ExamCheatModel(models.Model):
	COMMUNICATION = "Communication"
	IMPERSONATION = "Impersonation"

	EXAM_CHEAT_MODE_CHOICES = (
		(COMMUNICATION, "Communication"),
		(IMPERSONATION, "Impersonation"),
	)


class ExamConditionModel(models.Model):
	JOIN = "Join"
	LEAVE = "Leave"
	START = "Start"

	EXAM_CONDITION_CHOICES = (
		(JOIN, "Join"),
		(LEAVE, "Leave"),
		(START, "Start"),
	)


class ExamStatusModel(models.Model):
	COMPLETED = "Completed"
	STARTED = "Started"
	UPCOMING = "Upcoming"

	EXAM_STATUS_CHOICES = (
		(COMPLETED, "Completed"),
		(STARTED, "Started"),
		(UPCOMING, "Upcoming"),
	)


class ExamTypeModel(models.Model):
	ORAL = "Oral"
	WRITTEN = "Written"

	EXAM_TYPE_CHOICES = (
		(ORAL, "Oral"),
		(WRITTEN, "Written"),
	)


class OrganizationModel(models.Model):
	UC = "UC"
	UCY = "UCY"
	UPAT = "UPAT"

	ORGANIZATION_CHOICES = (
		(UC, "UC"),
		(UCY, "UCY"),
		(UPAT, "UPAT"),
	)


class RoleModel(models.Model):
	INSTRUCTOR = "INSTRUCTOR"
	STUDENT = "STUDENT"

	ROLE_CHOICES = (
		(INSTRUCTOR, "INSTRUCTOR"),
		(STUDENT, "STUDENT"),
	)


class VerificationStatusModel(models.Model):
	PENDING = "Pending"
	REQUESTED_MANUAL_APPROVAL = "Requested Manual Approval"
	VERIFIED = "Verified"

	VERIFICATION_STATUS_CHOICES = (
		(PENDING, "Pending"),
		(REQUESTED_MANUAL_APPROVAL, "Requested Manual Approval"),
		(VERIFIED, "Verified"),
	)


class MonitoringTypeModel(models.Model):
	IDENTIFICATION = "Identification"
	CHECKUP_PROCESS = "Checkup Process"
	EXAM_MONITORING = "Exam Monitoring"

	MONITORING_TYPE_CHOICES = (
		(IDENTIFICATION, "Identification"),
		(CHECKUP_PROCESS, "Checkup Process"),
		(EXAM_MONITORING, "Exam Monitoring"),
	)


class Users(AbstractBaseUser):
	email = models.EmailField(max_length=50, unique=True)
	name = models.CharField(max_length=500)
	organization = models.CharField(max_length=4, choices=OrganizationModel.ORGANIZATION_CHOICES)
	password = models.CharField(max_length=500)
	role = models.CharField(max_length=10, choices=RoleModel.ROLE_CHOICES)
	surname = models.CharField(max_length=500)
	ts_registration = models.DateTimeField(default=now)

	USERNAME_FIELD = 'email'


class LowContrast(models.Model):
	image = models.TextField(null=False)


class Examination(models.Model):
	additional_material = models.BooleanField(default=False)
	duration = models.BigIntegerField("Duration in minutes", default=0, null=False, validators=[MinValueValidator(0)])
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])
	name = models.CharField(max_length=50)
	exam_type = models.CharField(max_length=7, choices=ExamTypeModel.EXAM_TYPE_CHOICES)
	instructor_id = models.BigIntegerField(default=0, null=False)
	privacy_policy = models.TextField(null=True)
	scheduled_date = models.DateTimeField(null=True)
	ts_updated = models.DateTimeField(default=now)


class ExaminationConditionUpdate(models.Model):
	condition = models.CharField(max_length=5, choices=ExamConditionModel.EXAM_CONDITION_CHOICES)
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])


class ExaminationEnrollment(models.Model):
	details = JSONField()


class ExaminationStatus(models.Model):
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])
	instructor_id = models.BigIntegerField(default=0, null=False)
	status = models.CharField(max_length=9, choices=ExamStatusModel.EXAM_STATUS_CHOICES)
	student_id = models.BigIntegerField(default=0, null=False)
	verification_status = models.CharField(max_length=25, choices=VerificationStatusModel.VERIFICATION_STATUS_CHOICES, default=VerificationStatusModel.PENDING)
	is_manual_verification = models.BooleanField(default=False)
	ts_completed = models.DateTimeField(null=True)
	ts_enrolled = models.DateTimeField(default=now)
	ts_joined = models.DateTimeField(null=True)
	ts_quit = models.DateTimeField(null=True)
	ts_started = models.DateTimeField(null=True)
	ts_verified = models.DateTimeField(null=True)


class ManualApproveStudent(models.Model):
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])
	email = models.EmailField(max_length=50)


class MonitoringActivity(models.Model):
	user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
	)
	monitoring_type = models.CharField(max_length=15, choices=MonitoringTypeModel.MONITORING_TYPE_CHOICES, default=MonitoringTypeModel.EXAM_MONITORING)
	#alerts = JSONField(null=True)
	student_alerts = JSONField(null=True)
	exam_id = models.BigIntegerField(null=True, validators=[MinValueValidator(0)])
	ip_address = models.CharField(max_length=100, null=True, default='')
	identified_student = models.CharField(max_length=100, null=True, default='')
	predicted_label = models.CharField(max_length=100, null=True, default='')
	confidence_score = models.FloatField(null=True, default=0.0)
	image = models.TextField(null=True)
	running_processes = JSONField(null=True)
	not_allowed_apps = JSONField(null=True)
	session_id = models.CharField(max_length=50)
	is_face_detected = models.BooleanField(null=True)
	ts_added = models.DateTimeField(default=now)


class StudentFeedback(models.Model):
	user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
	)
	cheat_mode = models.CharField(max_length=13, choices=ExamCheatModel.EXAM_CHEAT_MODE_CHOICES)
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])
	feedback = models.TextField(null=False)
	session_id = models.CharField(max_length=50)
	ts_added = models.DateTimeField(default=now)


class RequestManualApproval(models.Model):
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])


class StudentProcesses(models.Model):
	running_processes = JSONField()


class StudentIdentification(models.Model):
	exam_id = models.BigIntegerField(null=False, validators=[MinValueValidator(0)])
	image = models.TextField(null=False)

