from django.urls import path, include
from django.contrib import admin
from exam import views
from exam import enrollment_views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),

    # Public pages
    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(template_name='exam/logout.html'), name='logout'),
    path('contactus', views.contactus_view, name='contactus'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    # Admin auth
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'), name='adminlogin'),

    # Admin dashboard
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),

    # Admin - Teachers
    path('admin-teacher', views.admin_teacher_view, name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view, name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view, name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view, name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view, name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view, name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view, name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view, name='reject-teacher'),

    # Admin - Students
    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-view-student', views.admin_view_student_view, name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view, name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view, name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view, name='delete-student'),

    # Admin - Courses
    path('admin-course', views.admin_course_view, name='admin-course'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view, name='admin-view-course'),
    path('update-course/<int:pk>', views.update_course_view, name='update-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),

    # Admin - Questions
    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view, name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view, name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('update-question/<int:pk>', views.update_question_view, name='update-question'),
    path('delete-question/<int:pk>', views.delete_question_view, name='delete-question'),

    # Admin - Enrollments
    path('admin-enrollments', enrollment_views.admin_enrollments_view, name='admin-enrollments'),
    path('admin-approve-enrollment/<int:pk>', enrollment_views.admin_approve_enrollment_view, name='admin-approve-enrollment'),
    path('admin-reject-enrollment/<int:pk>', enrollment_views.admin_reject_enrollment_view, name='admin-reject-enrollment'),

    # Admin - Other
    path('admin-proctoring-logs', views.admin_proctoring_logs_view, name='admin-proctoring-logs'),
    path('admin-contact-messages', views.admin_contact_messages_view, name='admin-contact-messages'),

    # Student - Courses & Enrollment
    path('routine', enrollment_views.exam_routine_view, name='exam-routine'),
    path('exam-routine', enrollment_views.exam_routine_view, name='exam-routine-alt'),
    path('courses', enrollment_views.course_list_view, name='course-list'),
    path('courses/<slug:slug>', enrollment_views.course_detail_view, name='course-detail'),
    path('enroll/<int:pk>', enrollment_views.enroll_course_view, name='enroll-course'),
    path('my-enrollments', enrollment_views.my_enrollments_view, name='my-enrollments'),
    path('payment-success/<int:payment_id>', enrollment_views.payment_success_view, name='payment-success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
