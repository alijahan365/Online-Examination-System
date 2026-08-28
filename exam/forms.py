from django import forms
from django.contrib.auth.models import User
from . import models
from teacher.models import Teacher

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=50)
    Email = forms.EmailField()
    recipient_type = forms.ChoiceField(
        choices=[('Admin', 'Admin'), ('Teacher', 'Specific Teacher')],
        initial='Admin',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'recipient_type_select'})
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
        empty_label="Select Teacher",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'teacher_select'})
    )
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

    def __init__(self, *args, **kwargs):
        super(ContactusForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(status=True)

class TeacherSalaryForm(forms.Form):
    salary = forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['course_name', 'question_number', 'total_marks', 'start_time', 'end_time', 'result_publish_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'result_publish_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(), empty_label="Course Name", to_field_name="id")
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['courseID'].queryset = models.Course.objects.all()

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'explanation']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'explanation': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'placeholder': '2-3 line explanation of the correct answer'})
        }


