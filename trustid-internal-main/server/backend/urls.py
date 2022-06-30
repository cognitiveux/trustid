from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

# Create the schema view for the API documentation
schema_view = get_schema_view(
	openapi.Info(
		title="TRUSTID API",
		default_version='v1',
		description="The endpoints for interacting with the TRUSTID server",
		terms_of_service="https://trustid-project.eu/",
		contact=openapi.Contact(email="admin@cognitiveux.com"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	url(r'^demo(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^demo/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	url('head_pose_classification', views.HeadPoseClassification.as_view(), name='head_pose_classification'),
	url('instructor/add_exam', views.AddExam.as_view(), name='instructor/add_exam'),
	url('instructor/enroll_students', views.EnrollStudents.as_view(), name='instructor/enroll_students'),
	url('instructor/list_exam', views.InstructorListExam.as_view(), name='instructor/list_exam'),
	url('instructor/manual_approve_student', views.InstructorManualApproveStudent.as_view(), name='instructor/manual_approve_student'),
	url('instructor/update_exam_details', views.UpdateExamDetails.as_view(), name='instructor/update_exam_details'),
	url('login', views.Login.as_view(), name='login'),
	url('monitoring', views.Monitoring.as_view(), name='monitoring'),
	url('refresh_token', views.RefreshToken.as_view(), name='refresh_token'),
	url('register_user', views.RegisterUser.as_view(), name='register_user'),
	url('student/check_verification_status', views.StudentCheckVerificationStatus.as_view(), name='student/check_verification_status'),
	url('student/checkup_process', views.StudentCheckupProcess.as_view(), name='student/checkup_process'),
	url('student/identification', views.StudentIdentification.as_view(), name='student/identification'),
	url('student/list_exam', views.StudentListExam.as_view(), name='student/list_exam'),
	url('student/request_manual_approval', views.StudentRequestManualApproval.as_view(), name='student/request_manual_approval'),
	url('student/submit_feedback', views.StudentSubmitFeedback.as_view(), name='student/submit_feedback'),
	url('trustid_version', views.TrustidVersion.as_view(), name='trustid_version'),
	url('update_exam_condition', views.ExamConditionUpdate.as_view(), name='update_exam_condition'),
	url('detect_low_contrast', views.DetectLowContrast.as_view(), name='detect_low_contrast'),
]

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
