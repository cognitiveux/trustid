# Generated by Django 2.2.17 on 2022-02-22 14:53

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('organization', models.CharField(choices=[('UC', 'UC'), ('UCY', 'UCY'), ('UPAT', 'UPAT')], max_length=4)),
                ('password', models.CharField(max_length=500)),
                ('role', models.CharField(choices=[('INSTRUCTOR', 'INSTRUCTOR'), ('STUDENT', 'STUDENT')], max_length=10)),
                ('surname', models.CharField(max_length=500)),
                ('ts_registration', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamCheatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ExamConditionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_material', models.BooleanField(default=False)),
                ('duration', models.BigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Duration in minutes')),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('name', models.CharField(max_length=50)),
                ('exam_type', models.CharField(choices=[('Oral', 'Oral'), ('Written', 'Written')], max_length=7)),
                ('instructor_id', models.BigIntegerField(default=0)),
                ('privacy_policy', models.TextField(null=True)),
                ('scheduled_date', models.DateTimeField(null=True)),
                ('ts_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationConditionUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(choices=[('Join', 'Join'), ('Leave', 'Leave'), ('Start', 'Start')], max_length=5)),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('instructor_id', models.BigIntegerField(default=0)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Started', 'Started'), ('Upcoming', 'Upcoming')], max_length=9)),
                ('student_id', models.BigIntegerField(default=0)),
                ('verification_status', models.CharField(choices=[('Pending', 'Pending'), ('Requested Manual Approval', 'Requested Manual Approval'), ('Verified', 'Verified')], default='Pending', max_length=25)),
                ('is_manual_verification', models.BooleanField(default=False)),
                ('ts_completed', models.DateTimeField(null=True)),
                ('ts_enrolled', models.DateTimeField(default=django.utils.timezone.now)),
                ('ts_joined', models.DateTimeField(null=True)),
                ('ts_quit', models.DateTimeField(null=True)),
                ('ts_started', models.DateTimeField(null=True)),
                ('ts_verified', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamStatusModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ExamTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='LowContrast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ManualApproveStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RequestManualApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentIdentification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentProcesses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('running_processes', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='VerificationStatusModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cheat_mode', models.CharField(choices=[('Communication', 'Communication'), ('Impersonation', 'Impersonation')], max_length=13)),
                ('exam_id', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('feedback', models.TextField()),
                ('session_id', models.CharField(max_length=50)),
                ('ts_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitoring_type', models.CharField(choices=[('Identification', 'Identification'), ('Checkup Process', 'Checkup Process'), ('Exam Monitoring', 'Exam Monitoring')], default='Exam Monitoring', max_length=15)),
                ('student_alerts', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('exam_id', models.BigIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('ip_address', models.CharField(default='', max_length=100, null=True)),
                ('identified_student', models.CharField(default='', max_length=100, null=True)),
                ('predicted_label', models.CharField(default='', max_length=100, null=True)),
                ('confidence_score', models.FloatField(default=0.0, null=True)),
                ('image', models.TextField(null=True)),
                ('running_processes', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('session_id', models.CharField(max_length=50)),
                ('ts_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
