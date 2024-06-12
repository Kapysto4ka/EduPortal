from django.shortcuts import render, redirect
from UserAuth.forms import *
from django.http import HttpResponse
from UserAuth.decorators import *
from django.utils import timezone
from django.db.models import Avg
from UserAuth.models import *
from django.shortcuts import render, get_object_or_404

@student_required
def index(request):
    student = request.user.student 
    current_date = timezone.now()  
    student_group = student.group

    total_assignments = Assignment.objects.filter(subject__group=student_group).count()
    completed_assignments = StudentAssignment.objects.filter(student=student, completed=True).count()
    graded_assignments = Grade.objects.filter(student=student).count()
    submitted_but_not_graded = StudentAssignment.objects.filter(student=student, completed=True).exclude(assignment__grades__student=student).count()
    assignments = Assignment.objects.filter(subject__group=student_group)
    pending_assignments = StudentAssignment.objects.filter(student=student, completed=True, graded=False).count()
    not_completed_assignments =  total_assignments - graded_assignments - pending_assignments

    for assignment in assignments:
        assignment.days_left = (assignment.deadline - current_date).days
        student_assignment = StudentAssignment.objects.filter(student=student, assignment=assignment).first()
        grade = Grade.objects.filter(student=student, assignment=assignment).first()
        assignment.grade = grade.grade if grade else None  

        if student_assignment:
            if grade:
                assignment.color = '#daffe5'  # Оцінені
            elif student_assignment.completed:
                assignment.color = '#fff1d6'  # Здані але не оцінені
            else:
                assignment.color = '#e9e7fd'  # Не здані
        else:
            if grade:
                assignment.color = '#daffe5'  # Оцінені, але не здані
            else:
                assignment.color = '#e9e7fd'  # Не здані

    context = {
        'student': student,
        'current_date': current_date,
        'total_assignments': total_assignments,
        'pending_assignments': pending_assignments,
        'not_completed_assignments': not_completed_assignments,
        'completed_assignments': completed_assignments,
        'graded_assignments': graded_assignments,
        'submitted_but_not_graded': submitted_but_not_graded,
        'assignments': assignments,
    }
    return render(request, "student/index.html", context)



@student_required
def change_avatar(request):
    student = request.user.student
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:user_profile', user_id=student.user.id)
    else:
        form = AvatarChangeForm(instance=student)
    
    return redirect('students:index')


@student_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student

    student_assignment = StudentAssignment.objects.filter(student=student, assignment=assignment).first()

    if request.method == "POST":
        if student_assignment and student_assignment.graded:
            return redirect('students:index') 

        student_assignment, created = StudentAssignment.objects.get_or_create(
            student=student,
            assignment=assignment,
        )
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=student_assignment)
        if form.is_valid():
            print('1')
            student_assignment = form.save(commit=False)
            student_assignment.submission_date = timezone.now()
            if not student_assignment.completed:
                student_assignment.completed = True
                student_assignment.submission_date = timezone.now()
            student_assignment.save()
            return redirect('students:index')
    else:
        form = AssignmentSubmissionForm(instance=student_assignment)

    context = {
        'assignment': assignment,
        'form': form,
        'completed': student_assignment.completed if student_assignment else False,
        'graded': student_assignment.graded if student_assignment else False,
        'file': student_assignment.file if student_assignment else None,
        'comment': student_assignment.comment if student_assignment else None,
    }
    return render(request, 'student/assignment_detail.html', context)

@student_required
def cancel_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student
    student_assignment = StudentAssignment.objects.filter(student=student, assignment=assignment).first()
    if student_assignment and not student_assignment.graded:
        student_assignment.delete()  
    return redirect('students:index')


@student_required
def user_profile(request, user_id):
    student = get_object_or_404(Student, user__id=user_id)
    return render(request, 'student/profile.html', {'student': student})

@student_required
def menu(request, name):
    current_date = timezone.now()
    student = request.user.student
    if name == 'grades':
        overall_average_grade = 0
        subjects_count = 0
        grades = Grade.objects.filter(student=student)

        subjects_grades = grades.values('assignment__subject__name').annotate(average_grade=Avg('grade'))

        subject_grades = Grade.objects.values('assignment__subject__name').annotate(average_grade=Avg('grade'))

        for subject in subjects_grades:
            subject['average_grade'] = round(subject['average_grade'], 2)
            overall_average_grade += round(subject['average_grade'], 2)
            subjects_count += 1

        if subjects_count > 0:
            overall_average_grade = round(overall_average_grade / subjects_count, 2)
        else:
            overall_average_grade = 0

        context = {
            'average_grade_all_subjects': overall_average_grade,
            'grades': grades,
            'subjects_grades': subjects_grades,
        }
        return render(request, "student/grades.html", context)
    elif name == 'calendar':
        context = {
            'current_date': current_date,
        }
        return render(request, "student/calendar.html", context)
    elif name == 'calendar':
        context = {
            'current_date': current_date,
        }
        return render(request, "student/calendar.html", context)
    elif name == 'contacts':
        context = {
            'current_date': current_date,
        }
        return render(request, "student/contacts.html", context)