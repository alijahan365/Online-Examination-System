from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

from django.utils import timezone

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    now = timezone.now()
    
    course_list = []
    for c in courses:
        status = 'LIVE'
        if c.start_time and now < c.start_time:
            status = 'SCHEDULED'
        elif c.end_time and now > c.end_time:
            status = 'CLOSED'
        
        course_list.append({
            'course': c,
            'status': status
        })
        
    return render(request, 'student/student_exam.html', {'course_list': course_list, 'now': now})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    now = timezone.now()
    if course.start_time and now < course.start_time:
        return redirect('student-exam')
    if course.end_time and now > course.end_time:
        return redirect('student-exam')

    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)    
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks

    now = timezone.now()
    results_published = True
    if course.result_publish_time and now < course.result_publish_time:
        results_published = False
    
    return render(request,'student/check_marks.html',{
        'course': course,
        'results': results,
        'questions': questions,
        'total_marks': total_marks,
        'results_published': results_published,
        'now': now
    })

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_ask_doubt_view(request):
    student = models.Student.objects.get(user_id=request.user.id)
    teachers = TMODEL.Teacher.objects.all()
    doubts = models.StudentDoubt.objects.filter(student=student).order_by('-created_at')

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        question_text = request.POST.get('question_text')
        if teacher_id and question_text:
            teacher = TMODEL.Teacher.objects.get(id=teacher_id)
            models.StudentDoubt.objects.create(
                student=student,
                teacher=teacher,
                question_text=question_text
            )
            return redirect('ask-doubt')

    return render(request, 'student/student_doubts.html', {'teachers': teachers, 'doubts': doubts})



import base64
import time
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def log_cheating_event_view(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id') or request.COOKIES.get('course_id')
        reason = request.POST.get('reason', 'Suspicious Activity Detected')
        image_data = request.POST.get('image_data')

        student = models.Student.objects.get(user_id=request.user.id)
        course_name = "Online Exam"
        if course_id:
            try:
                course = QMODEL.Course.objects.get(id=course_id)
                course_name = course.course_name
            except QMODEL.Course.DoesNotExist:
                pass
        
        cheating_log = models.CheatingLog(
            student=student,
            course_name=course_name,
            reason=reason
        )

        if image_data and ';base64,' in image_data:
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                if ext == 'jpeg':
                    ext = 'jpg'
                file_name = f"cheating_{student.id}_{int(time.time())}.{ext}"
                cheating_log.snapshot.save(file_name, ContentFile(base64.b64decode(imgstr)), save=False)
            except Exception as e:
                pass

        cheating_log.save()
        return JsonResponse({'status': 'success', 'message': 'Violation logged'})
    return JsonResponse({'status': 'failed'}, status=400)


from exam.views import get_grouped_proctoring_logs

@login_required
def proctoring_logs_view(request):
    grouped_logs = get_grouped_proctoring_logs()
    
    if request.user.is_superuser or request.user.is_staff:
        base_template = 'exam/adminbase.html'
    elif TMODEL.Teacher.objects.filter(user=request.user).exists():
        base_template = 'teacher/teacherbase.html'
    else:
        base_template = 'exam/adminbase.html'

    return render(request, 'student/proctoring_logs.html', {'grouped_logs': grouped_logs, 'base_template': base_template})





  