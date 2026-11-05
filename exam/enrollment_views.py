from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages as django_messages
from django.utils import timezone
from django.http import JsonResponse
from . import models
from student import models as SMODEL


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def course_list_view(request):
    """Public course listing page"""
    courses = models.Course.objects.filter(is_active=True).order_by('-created_at')
    categories = models.CourseCategory.objects.all()

    # For each course, check if student is enrolled
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    enrolled_course_ids = models.Enrollment.objects.filter(
        student=student, status='active'
    ).values_list('course_id', flat=True)

    selected_category = request.GET.get('category')
    if selected_category:
        courses = courses.filter(category__slug=selected_category)

    return render(request, 'exam/course_list.html', {
        'courses': courses,
        'categories': categories,
        'enrolled_course_ids': list(enrolled_course_ids),
        'selected_category': selected_category,
    })


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def course_detail_view(request, slug):
    """Course detail page — shows subjects and enrollment CTA"""
    course = get_object_or_404(models.Course, slug=slug, is_active=True)
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    subjects = models.Subject.objects.filter(course=course, is_active=True)

    enrollment = models.Enrollment.objects.filter(
        student=student, course=course
    ).first()

    is_enrolled = enrollment and enrollment.is_valid()

    return render(request, 'exam/course_detail.html', {
        'course': course,
        'subjects': subjects,
        'enrollment': enrollment,
        'is_enrolled': is_enrolled,
    })


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def enroll_course_view(request, pk):
    """Handle course enrollment request"""
    course = get_object_or_404(models.Course, id=pk, is_active=True)
    student = SMODEL.Student.objects.get(user_id=request.user.id)

    # Check if already enrolled
    existing = models.Enrollment.objects.filter(student=student, course=course).first()
    if existing and existing.is_valid():
        django_messages.info(request, 'তুমি ইতিমধ্যে এই কোর্সে এনরোলড আছ।')
        return redirect('student-exam')

    if request.method == 'POST':
        if course.is_free or course.price == 0:
            # Free course: auto-approve enrollment
            enrollment, created = models.Enrollment.objects.get_or_create(
                student=student, course=course,
                defaults={'status': 'active'}
            )
            if not created:
                enrollment.status = 'active'
                enrollment.save()

            # Create payment record for free
            models.Payment.objects.get_or_create(
                enrollment=enrollment,
                defaults={
                    'amount': 0,
                    'method': 'free',
                    'status': 'completed',
                    'paid_at': timezone.now()
                }
            )
            django_messages.success(request, f'"{course.course_name}" কোর্সে সফলভাবে এনরোল হয়েছ!')
            return redirect('student-exam')
        else:
            # Paid course: create pending enrollment + show payment form
            enrollment, created = models.Enrollment.objects.get_or_create(
                student=student, course=course,
                defaults={'status': 'pending'}
            )
            method = request.POST.get('payment_method', 'bkash')
            txn_id = request.POST.get('transaction_id', '').strip()

            payment, _ = models.Payment.objects.get_or_create(
                enrollment=enrollment,
                defaults={
                    'amount': course.price,
                    'method': method,
                    'transaction_id': txn_id,
                    'status': 'pending',
                }
            )
            if not _:
                payment.method = method
                payment.transaction_id = txn_id
                payment.status = 'pending'
                payment.save()

            django_messages.success(
                request,
                f'পেমেন্ট রিকোয়েস্ট পাঠানো হয়েছে। অ্যাডমিন ভেরিফাই করার পর তুমি এক্সামে প্রবেশ করতে পারবে।'
            )
            return redirect('my-enrollments')

    return render(request, 'exam/enroll_course.html', {
        'course': course,
        'student': student,
    })


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def my_enrollments_view(request):
    """Student's enrolled courses"""
    student = SMODEL.Student.objects.get(user_id=request.user.id)
    enrollments = models.Enrollment.objects.filter(student=student).select_related('course', 'payment').order_by('-enrolled_at')
    return render(request, 'exam/my_enrollments.html', {
        'enrollments': enrollments,
    })


# ---- Admin enrollment management ----

@login_required(login_url='adminlogin')
def admin_enrollments_view(request):
    """Admin view: all enrollments with payment details"""
    enrollments = models.Enrollment.objects.all().select_related(
        'student', 'course', 'payment'
    ).order_by('-enrolled_at')
    return render(request, 'exam/admin_enrollments.html', {'enrollments': enrollments})


@login_required(login_url='adminlogin')
def admin_approve_enrollment_view(request, pk):
    """Admin approves a pending enrollment"""
    enrollment = get_object_or_404(models.Enrollment, id=pk)
    enrollment.status = 'active'
    enrollment.save()

    if hasattr(enrollment, 'payment'):
        enrollment.payment.status = 'completed'
        enrollment.payment.paid_at = timezone.now()
        enrollment.payment.save()

    django_messages.success(request, f'{enrollment.student.get_name}-এর এনরোলমেন্ট অনুমোদন করা হয়েছে।')
    return redirect('admin-enrollments')


@login_required(login_url='adminlogin')
def admin_reject_enrollment_view(request, pk):
    """Admin rejects/cancels an enrollment"""
    enrollment = get_object_or_404(models.Enrollment, id=pk)
    enrollment.status = 'cancelled'
    enrollment.save()

    if hasattr(enrollment, 'payment'):
        enrollment.payment.status = 'failed'
        enrollment.payment.save()

    django_messages.success(request, f'এনরোলমেন্ট বাতিল করা হয়েছে।')
    return redirect('admin-enrollments')
