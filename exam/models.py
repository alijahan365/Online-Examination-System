from django.db import models
from django.utils.text import slugify
from student.models import Student
from teacher.models import Teacher


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default='fas fa-book')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Course Categories"


class Course(models.Model):
    # --- Existing fields (kept for backward compatibility) ---
    course_name = models.CharField(max_length=200)
    question_number = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_publish_time = models.DateTimeField(null=True, blank=True)

    # --- New LMS fields ---
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True)
    negative_marking = models.FloatField(default=0.25)
    routine_date = models.DateField(null=True, blank=True)
    routine_syllabus = models.TextField(blank=True, default='')
    batch_title = models.CharField(max_length=150, blank=True, default='')
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.course_name)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['-created_at']


class Subject(models.Model):
    """Chapter/Module under a Course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        teacher_name = f" ({self.teacher.get_name})" if self.teacher else ""
        return f"{self.course.course_name} → {self.title}{teacher_name}"

    class Meta:
        ordering = ['order']


class Exam(models.Model):
    """Specific Exam under a Subject"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    question_number = models.PositiveIntegerField(default=10)
    total_marks = models.PositiveIntegerField(default=50)
    pass_marks = models.PositiveIntegerField(default=20)
    duration_minutes = models.PositiveIntegerField(default=30)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_publish_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.subject and not self.course:
            self.course = self.subject.course
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.title} → {self.name}"

    class Meta:
        ordering = ['-created_at']


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def is_valid(self):
        from django.utils import timezone
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    def __str__(self):
        return f"{self.student} → {self.course.course_name} ({self.status})"


class Payment(models.Model):
    METHOD_CHOICES = [
        ('bkash', 'bKash (01784299242)'),
        ('rocket', 'Rocket (01626796685)'),
        ('nagad', 'Nagad'),
        ('card', 'Islami Bank Visa Debit Card'),
        ('free', 'Free Course'),
        ('manual', 'Manual/Admin Approval'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('completed', 'Completed / Verified'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='bkash')
    transaction_id = models.CharField(max_length=100, blank=True)
    sender_number = models.CharField(max_length=50, blank=True, default='')
    card_last4 = models.CharField(max_length=10, blank=True, default='')
    bank_name = models.CharField(max_length=100, blank=True, default='Islami Bank Bangladesh Limited')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def invoice_no(self):
        return f"INV-{self.created_at.strftime('%Y%m')}-{self.id:04d}"

    def __str__(self):
        return f"{self.enrollment.student} - {self.amount} BDT via {self.get_method_display()} ({self.status})"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    exam_paper = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    marks = models.PositiveIntegerField(default=1)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)
    explanation = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)

    def __str__(self):
        return self.question[:80]


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    wrong_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)
    negative_marks = models.FloatField(default=0.0)
    net_marks = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)
    is_practice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.exam.course_name} ({self.marks})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    recipient_type = models.CharField(max_length=20, default='Admin')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} -> {self.recipient_type} ({self.created_at.strftime('%d %b %Y')})"
