from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'created_at')
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson', 'points')
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'total_possible', 'submitted_at')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
