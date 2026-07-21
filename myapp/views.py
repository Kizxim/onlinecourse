from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Question, Choice, Submission

def index(request):
    courses = Course.objects.all()
    return render(request, 'myapp/index.html', {'courses': courses})

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'myapp/course_details_bootstrap.html', {'course': course})

@login_required
def exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    return render(request, 'myapp/exam.html', {'lesson': lesson, 'questions': questions})

@login_required
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    
    score = 0
    total = 0
    answers = {}
    
    for question in questions:
        total += question.points
        selected = request.POST.get(f'question_{question.id}')
        if selected:
            selected_choice = Choice.objects.get(id=selected)
            if selected_choice.is_correct:
                score += question.points
            answers[str(question.id)] = selected
    
    submission = Submission.objects.create(
        student=request.user,
        lesson=lesson,
        answers=answers,
        score=score,
        total_possible=total
    )
    
    return redirect('show_exam_result', submission_id=submission.id)

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    passed = submission.score >= submission.total_possible * 0.7
    
    return render(request, 'myapp/result.html', {
        'submission': submission,
        'passed': passed
    })
