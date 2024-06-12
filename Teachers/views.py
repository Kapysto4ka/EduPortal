from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from UserAuth.decorators import teacher_required
from .forms import SubjectForm, AssignmentForm, GradeForm, AttendanceForm
from UserAuth.forms import *
from UserAuth.models import *
from django.utils import timezone
from calendar import monthrange 
from datetime import datetime
from django.utils.dateparse import parse_date
current_date = timezone.now() 

@teacher_required
def teacher_dashboard(request):
    current_date = timezone.now()  
    teacher = request.user.teacher
    groups = teacher.groups.all()
    subjects = teacher.subjects.all()
    
    context = {
        'current_date': current_date,
        'teacher': teacher,
        'groups': groups,
        'subjects': subjects,
    }
    
    return render(request, 'teacher/dashboard.html', context)


@teacher_required
def group_detail(request, group_id):
    current_date = timezone.now()  
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    
    assignments = []
    for subject in group.subjects.all():
        assignments.extend(subject.assignments.all())
    
    attendance_records = Attendance.objects.filter(subject__group=group)
    
    context = {
        'current_date': current_date,
        'group': group,
        'students': students,
        'assignments': assignments,
        'attendance_records': attendance_records,
    }
    
    return render(request, 'teacher/group_detail.html', context)

@teacher_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    group_id = assignment.subject.group.id
    if request.method == "POST":
        assignment.delete()
        return redirect('teachers:group_detail', group_id=group_id)
    return redirect('teachers:assignment_detail', assignment_id=assignment.id)

@teacher_required
def attendance_overview(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    subjects = Subject.objects.filter(group=group)

    selected_subject_id = None
    selected_month = None
    days_in_month = []
    attendance_data = {}

    if request.method == "POST":
        selected_month = request.POST.get("month")
        selected_subject_id = request.POST.get("subject")
        if selected_month and selected_subject_id:
            year, month = map(int, selected_month.split('-'))
            _, days_in_month = monthrange(year, month)
            days_in_month = [str(day).zfill(2) for day in range(1, days_in_month + 1)]
            attendance_records = Attendance.objects.filter(subject_id=selected_subject_id, date__year=year, date__month=month)

            attendance_data = {student.id: {day: None for day in days_in_month} for student in students}
            for record in attendance_records:
                day = record.date.strftime("%d")
                attendance_data[record.student.id][day] = '' if record.present else 'н'
    
    context = {
        'current_date': current_date,
        'group': group,
        'students': students,
        'subjects': subjects,
        'days_in_month': days_in_month,
        'attendance_data': attendance_data,
        'selected_subject_id': selected_subject_id,
        'selected_month': selected_month,
    }

    return render(request, 'teacher/attendance_overview.html', context)



@teacher_required
def change_avatar(request):
    teacher = request.user.teacher
    if request.method == 'POST':
        form = TeacherAvatarChangeForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:user_profile', user_id=teacher.user.id)
    else:
        form = TeacherAvatarChangeForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
    }
    return render(request, 'teachers/change_avatar.html', context)


@teacher_required
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers:dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'your_template.html', {'form': form})

@teacher_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    students = assignment.subject.group.students.all()
    
    student_assignments = StudentAssignment.objects.filter(assignment=assignment, completed=True)
    
    if request.method == "POST":
        student_id = request.POST.get("student")
        grade_value = request.POST.get("grade")
        student = get_object_or_404(Student, id=student_id)
        
        student_assignment, created = StudentAssignment.objects.get_or_create(
            student=student, assignment=assignment,
            defaults={'completed': False, 'graded': True}
        )
        
        if not created: 
            student_assignment.graded = True
            student_assignment.save()

        grade_exists = Grade.objects.filter(student=student, assignment=assignment).exists()
        if grade_exists:
            Grade.objects.filter(student=student, assignment=assignment).update(grade=grade_value)
        else:
            Grade.objects.create(student=student, assignment=assignment, grade=grade_value)
        
        return redirect('teachers:assignment_detail', assignment_id=assignment.id)
    
    context = {
        'current_date': current_date,
        'assignment': assignment,
        'students': students,
        'student_assignments': student_assignments,
    }
    return render(request, 'teacher/assignment_detail.html', context)



@teacher_required
def user_profile(request, user_id):
    teacher = get_object_or_404(Teacher, user__id=user_id)
    return render(request, 'teacher/profile.html', {'teacher': teacher})


@teacher_required
def view_grades(request, group_id):
    teacher = request.user.teacher
    group = get_object_or_404(Group, id=group_id)
    subjects = teacher.subjects.filter(group=group)
    students = Student.objects.filter(group=group)

    selected_subject = None
    selected_student = None
    grades = []
    average_grade = None

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        selected_subject = get_object_or_404(Subject, id=subject_id)
        selected_student = get_object_or_404(Student, id=student_id)
        grades = Grade.objects.filter(student=selected_student, assignment__subject=selected_subject)

        if grades.exists():
            average_grade = grades.aggregate(models.Avg('grade'))['grade__avg']
            average_grade = round(average_grade,2)
    context = {
        'current_date': current_date,
        'group': group,
        'subjects': subjects,
        'students': students,
        'selected_subject': selected_subject,
        'selected_student': selected_student,
        'grades': grades,
        'average_grade': average_grade,
    }

    return render(request, 'teacher/students_grades.html', context)


@teacher_required
def create_assignment(request, group_id):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.subject_id = Subject.objects.filter(group_id=group_id).first().id
            assignment.teacher_id = request.user.teacher.id
            assignment.save()
            return redirect('teachers:group_detail', group_id=group_id)
    else:
        form = AssignmentForm()
    context = {
            'current_date': current_date,
            'form': form,
        }
    return render(request, 'teacher/create_assignment.html', context)




@teacher_required
def menu(request, name):
    current_date = timezone.now()  
    if name == 'contacts':
        context = {
            'current_date': current_date,
        }
        return render(request, "student/contacts.html", context)
    elif name == 'calendar':
        context = {
            'current_date': current_date,
        }
        return render(request, "student/calendar.html", context)
    elif name == 'subject':
        print('Entering create_subject view')
        if request.method == 'POST':
            print("POST request received")
            form = SubjectForm(request.POST)
            if form.is_valid():
                print("Form is valid")
                subject = form.save(commit=False)
                subject.save()
                form.save_m2m()
                return redirect('teachers:dashboard')
            else:
                print("Form is not valid:", form.errors)
        else:
            print("GET request received")
            form = SubjectForm()
        return render(request, 'teacher/create_subject.html', {'form': form})