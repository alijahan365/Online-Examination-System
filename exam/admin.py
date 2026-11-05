from django.contrib import admin
from . import models


@admin.register(models.CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'category', 'teacher', 'price', 'is_free', 'is_active', 'created_at']
    list_filter = ['is_free', 'is_active', 'category']
    search_fields = ['course_name', 'description']
    prepopulated_fields = {'slug': ('course_name',)}
    list_editable = ['is_free', 'is_active']


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active']
    list_filter = ['course', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrolled_at']
    list_filter = ['status']
    search_fields = ['student__user__first_name', 'course__course_name']
    list_editable = ['status']
    actions = ['approve_enrollments', 'cancel_enrollments']

    def approve_enrollments(self, request, queryset):
        from django.utils import timezone
        for enrollment in queryset:
            enrollment.status = 'active'
            enrollment.save()
            if hasattr(enrollment, 'payment'):
                enrollment.payment.status = 'completed'
                enrollment.payment.paid_at = timezone.now()
                enrollment.payment.save()
        self.message_user(request, f'{queryset.count()} enrollment(s) approved.')
    approve_enrollments.short_description = "Approve selected enrollments"

    def cancel_enrollments(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_enrollments.short_description = "Cancel selected enrollments"


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'amount', 'method', 'status', 'transaction_id', 'paid_at']
    list_filter = ['status', 'method']
    search_fields = ['transaction_id', 'enrollment__student__user__first_name']
    list_editable = ['status']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'course', 'subject', 'marks', 'answer']
    list_filter = ['course', 'subject']
    search_fields = ['question']


@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks', 'is_practice', 'date']
    list_filter = ['exam', 'is_practice']


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'recipient_type', 'created_at']
    list_filter = ['recipient_type']
    readonly_fields = ['created_at']
