from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from SDMSapp.models import Student, Stud_item
from .forms import *
from django.http import JsonResponse
from django.views import View
from .forms import SearchForm
from django.contrib import messages
from django.shortcuts import render, redirect
from SDMSapp.models import Student, Programme, Department  # Import your models
from .forms import *
from datetime import datetime
from django.http import HttpResponse
from django.db.utils import IntegrityError

#from .forms import PlayerForm, Player, DepartmentForm, Sportform


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Handle invalid login
            return render(request, 'SDMSapp/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'SDMSapp/login.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'SDMSapp/signup.html', {'form': form})

@login_required
def user_home(request):
    student={
        'student':Student.objects.all
    }
    return render(request, 'SDMSapp/home.html',student)


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_student') 
    else:
        form = StudentForm()
    return render(request, 'SDMSapp/addstudent.html', {'form': form})

def success_page(request):
    return render(request, 'SDMSapp/success_page.html')

def view_student(request):
    # Query all student records
    students = Student.objects.all()
    return render(request, 'SDMSapp/view_student.html', {'students': students})

def search_student(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            uty_reg_no = form.cleaned_data['uty_reg_no']
            return redirect('edit_student', uty_reg_no=uty_reg_no)
    else:
        form = SearchForm()
    return render(request, 'search_student.html', {'form': form})


@login_required
def edit_student_form(request):
    if request.method == 'POST':
        uty_reg_no = request.POST.get('uty_reg_no')
        if Student.objects.filter(uty_reg_no=uty_reg_no).exists():
            return redirect('edit_student', uty_reg_no=uty_reg_no)
        else:
            messages.error(request, "Student ID not found.")
            return redirect('edit_student_form')
    return render(request, 'SDMSapp/edit_student_form.html')

@login_required
def edit_student(request, uty_reg_no):
    if request.method == 'POST':
        name = request.POST.get('name')
        year_of_admission = request.POST.get('year_of_admission')
        admission_no = request.POST.get('admission_no')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        phone_number = request.POST.get('phone_number')
        aadhar_number = request.POST.get('aadhar_number')
        dob = request.POST.get('dob')
        programme_id = request.POST.get('programme_id')
        place = request.POST.get('place')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')

        department_id = request.POST.get('department')
        department = get_object_or_404(Department, dept_name=department_id)
        programme = get_object_or_404(Programme, id=programme_id)

        edit = get_object_or_404(Student, uty_reg_no=uty_reg_no)
        edit.name = name
        edit.year_of_admission = year_of_admission
        edit.admission_no = admission_no
        edit.gender = gender
        edit.programme_id = programme
        edit.place = place
        edit.department = department
        edit.phone_number = phone_number
        edit.aadhar_number = aadhar_number
        edit.dob = dob
        edit.city = city
        edit.district = district
        edit.pincode = pincode
        edit.save()

        messages.info(request, "Data Updated Successfully")
        return redirect("/")

    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    departments = Department.objects.all()
    programmes = Programme.objects.all()
    context = {"student": student, "departments": departments, "programmes": programmes}
    return render(request, 'SDMSapp/edit_student.html', context)

@login_required
def delete_student(request, uty_reg_no):
    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('view_student')

@login_required
def confirm_delete_student(request, uty_reg_no):
    student = get_object_or_404(Student, uty_reg_no=uty_reg_no)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('view_student')
    return render(request, 'SDMSapp/confirm_delete_student.html', {'student': student})

def user_logout(request):
    logout(request)
    return redirect('home')    

@login_required
def assign_student(request):
    if request.method == 'POST':
        form = Assign_StudentForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('assignview_student')
    else:
        form = Assign_StudentForm()
    return render(request, 'SDMSapp/assign_student.html', {'form': form})

def assignview_student(request):
        query = request.GET.get('q')
        if query:
            assignments = Stud_item.objects.filter(
                Q(stud__name__icontains=query) |
                Q(stud__uty_reg_no__icontains=query) |
                Q(item__item_name__icontains=query)
            )
        else:
            assignments = Stud_item.objects.all()
        return render(request, 'SDMSapp/search_assignments.html', {'assignments': assignments, 'query': query})

@login_required
def confirm_assign_delete(request, stud_id):
    stud_item = get_object_or_404(Stud_item, id = stud_id)
    if request.method == 'GET':
        stud_item.delete()
        return redirect('assignview_student')
    return render(request, 'SDMSapp/assign_view.html', {'stud_item': stud_item})

@login_required
def view_items(request):
    items = Item.objects.all()
    years = Stud_item.objects.values_list('year', flat=True).distinct()
    return render(request, 'SDMSapp/view_items.html', {'items': items, 'years': years})


def view_players(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    selected_year = request.GET.get('year', '')  # Get selected year from query params
    selected_gender = request.GET.get('gender', '')  # Get selected gender from query params
    
    # Filter students based on item_id and optionally on selected year
    stud_items = Stud_item.objects.filter(item_id=item_id)
    
    # Apply additional filter based on selected year
    if selected_year:
        stud_items = stud_items.filter(year=selected_year)
    
    # Apply additional filter based on selected gender
    if selected_gender:
        stud_items = stud_items.filter(stud__gender=selected_gender)

    context = {
        'item': item,
        'stud_items': stud_items,
        'selected_year': selected_year,
        'selected_gender': selected_gender,
    }
    return render(request, 'SDMSapp/view_players.html', context)

@login_required
def edit_assign(request, id):
    stud_item = get_object_or_404(Stud_item, id=id)
    if request.method == 'POST':
        form = AssignStudentForm(request.POST, instance=stud_item)
        if form.is_valid():
            form.save()
            return redirect('view_players', item_id=stud_item.item.id)
    else:
        form = AssignStudentForm(instance=stud_item)
    return render(request, 'SDMSapp/edit_assign.html', {'form': form})

@login_required
def edit_assignment(request, pk):
    stud_item = get_object_or_404(Stud_item, pk=pk)
    if request.method == 'POST':
        form = StudItemForm(request.POST, instance=stud_item)
        if form.is_valid():
            form.save()
            return redirect('view_items')
    else:
        form = StudItemForm(instance=stud_item)
    return render(request, 'SDMSapp/edit_assignment.html', {'form': form})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            if not date:
                date = 'Not filled'  # Set date to "Not filled" if it's empty
            try:
                form.save()
                return redirect('success_page')
            except IntegrityError:
                # Handle IntegrityError if needed
                pass
    else:
        form = AttendanceForm()
    return render(request, 'SDMSapp/mark_attendance.html', {'form': form})

def get_items_by_student(request):
    student_id = request.GET.get('student_id')
    items = Item.objects.filter(stud_item__student_id=student_id).values('id', 'item_name')
    return JsonResponse(list(items), safe=False)

@login_required
def view_attendance(request):
    # Get attendance records for the selected date if provided
    date = request.GET.get('date', None)
    if date:
        attendance_records = Attendance.objects.filter(date=date)
    else:
        attendance_records = Attendance.objects.all()

    return render(request, 'SDMSapp/view_attendance.html', {'attendance_records': attendance_records, 'selected_date': date})


@login_required
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'GET':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('view_attendance')  # Replace with your attendance list view name
    else:
        return redirect('view_attendance')


def upload_picture(request):
    if request.method == 'POST':
        form = PictureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_picture')
    else:
        form = PictureUploadForm()
    return render(request, 'SDMSapp/upload_picture.html', {'form': form})

def view_pictures(request):
    items = Item.objects.all()
    pictures = []
    current_year = datetime.now().year
    if 'item' in request.GET and 'year' in request.GET:
        item_id = request.GET.get('item')
        year = request.GET.get('year')
        pictures = Picture.objects.filter(item_id=item_id, year=year)
    return render(request, 'SDMSapp/view_picture.html', {'items': items, 'pictures': pictures, 'current_year': current_year})

def download_picture(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    response = HttpResponse(picture.image, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{picture.image.name}"'
    return response

@login_required
def assign_players(request):
    if request.method == 'POST':
        form = AssignStudentForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            students = form.cleaned_data['students']
            gender = form.cleaned_data['gender']
            player_status = form.cleaned_data['player_status']
            uty_team_selection = form.cleaned_data['uty_team_selection']
            position = form.cleaned_data['position']
            year = form.cleaned_data['year']

            for student in students:
                Stud_item.objects.create(
                    stud=student,
                    item=item,
                    gender=gender,
                    player_status=player_status,
                    uty_team_selection=uty_team_selection,
                    position=position,
                    year=year
                )

            return redirect('success_page')  # Redirect to success page after assigning
        else:
            print(form.errors)  # Print form errors to console for debugging
    else:
        form = AssignStudentForm()
    return render(request, 'SDMSapp/assign_players.html', {'form': form})

def view_profile(request, uty_reg_no):
    student = Student.objects.get(uty_reg_no=uty_reg_no)
    sports_details = Stud_item.objects.filter(stud=student).order_by('year')
    
    sports_details_by_year = {}
    for detail in sports_details:
        year = detail.year
        if year not in sports_details_by_year:
            sports_details_by_year[year] = []
        sports_details_by_year[year].append(detail)

    context = {
        'student': student,
        'sports_details': sports_details_by_year,
    }
    return render(request, 'SDMSapp/profile.html', context)



def manage_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificate_list')
    else:
        form = CertificateForm()
    return render(request, 'SDMSapp/manage_certificate.html', {'form': form})

def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'SDMSapp/certificate_list.html', {'certificates': certificates})

def hod_profile(request):
    return render(request, 'SDMSapp/hod_profile.html')

def edit_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if request.method == 'POST':
        form = CertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('certificate_list')  # Redirect to certificate list page
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'SDMSapp/edit_certificate.html', {'form': form})
    
def delete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if request.method == 'POST':
        certificate.delete()
        return redirect('certificate_list')  # Redirect to certificate list page
    return render(request, 'SDMSapp/delete_certificate.html', {'certificate': certificate})

@login_required
def student_grace_marks(request):
    year = request.GET.get('year', None)
    stud_items = []

    if year:
        stud_items = Stud_item.objects.filter(year=year)
        # Filter out students with zero grace marks and calculate grace marks
        filtered_stud_items = []
        for item in stud_items:
            grace_mark = calculate_grace_mark(item.uty_team_selection, item.position)
            if grace_mark > 0:
                filtered_stud_items.append({
                    'stud': item.stud.name,
                    'item': item.item.item_name,
                    'uty_team_selection': item.uty_team_selection,
                    'position': item.position,
                    'grace_mark': grace_mark
                })
        stud_items = filtered_stud_items

    context = {
        'year': year,
        'stud_items': stud_items,
    }
    return render(request, 'SDMSapp/student_grace_mark.html', context)


def calculate_grace_mark(team_selection, position):
    grace_marks_map = {
        'Selected': {
            'default': 7,
            '3': 8,
            '2': 9,
            '1': 10
        },
        'Not Selected': {
            '1': 6,
            '2': 5,
            '3': 4,
            'default': 0
        }
    }

    if team_selection in grace_marks_map:
        return grace_marks_map[team_selection].get(str(position), grace_marks_map[team_selection]['default'])

    return 0

def get_student_details(request):
    student_id = request.GET.get('student_id', None)
    data = {}

    if student_id:
        try:
            student = Student.objects.get(id=student_id)
            data['year'] = student.year
            data['programme_id'] = student.programme_id.id  # Assuming you want the ID
            data['department'] = student.department.name  # Assuming you want the department name

            # Fetch items assigned to this student
            items = Item.objects.filter(student=student)
            data['items'] = list(items.values('id', 'item_name'))

        except Student.DoesNotExist:
            data['error'] = 'Student not found'

    return JsonResponse(data)