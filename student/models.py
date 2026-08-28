from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def student_id(self):
        return f"STD-{self.id:04d}"
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return f"{self.student_id} - {self.user.first_name}"

class CheatingLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=255)
    snapshot = models.ImageField(upload_to='cheating_snapshots/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_name} - {self.course_name} ({self.reason})"

class StudentDoubt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)
    question_text = models.TextField()
    reply_text = models.TextField(blank=True, default='')
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doubt by {self.student.get_name} to {self.teacher.get_name}"