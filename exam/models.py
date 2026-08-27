from django.db import models
from student.models import Student
from teacher.models import Teacher

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    recipient_type = models.CharField(max_length=20, default='Admin')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} -> {self.recipient_type} ({self.created_at.strftime('%d %b %Y')})"

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_publish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.course_name

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer = models.CharField(max_length=200, choices=cat)
    explanation = models.TextField(blank=True, default='')

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


