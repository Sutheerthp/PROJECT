# forms.py
from django import forms
from .models import *
from django.core.validators import RegexValidator

class StudentForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    class Meta:
        model = Student
        fields = '__all__'


class TeamForm(forms.ModelForm):
    class meta:
        model = Stud_item
        fields = '__all__'

class Assign_StudentForm(forms.ModelForm):
    class Meta:
        model = Stud_item
        fields = ['stud', 'item', 'player_status', 'uty_team_selection', 'position', 'year']

    stud = forms.ModelChoiceField(queryset=Student.objects.all())
    item = forms.ModelChoiceField(queryset=Item.objects.all())

class SearchForm(forms.Form):
    uty_reg_no = forms.CharField(label='Enter Registration Number', max_length=50)

class AssignStudentForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Stud_item
        fields = ['item', 'gender', 'player_status', 'uty_team_selection', 'position', 'year', 'students']

class StudItemForm(forms.ModelForm):
    class Meta:
        model = Stud_item
        fields = ['stud', 'item', 'player_status', 'uty_team_selection', 'position', 'year']


class AttendanceForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'item', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5']

class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['item', 'year', 'image']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
# class DepartmentForm(forms.ModelForm):
#     class Meta:
#         model = Department
#         fields = '__all__'

# class Sportform(forms.ModelForm):
#     class Meta:
#         model = Sport
#         fields = '__all__'


# class PlayerForm(forms.ModelForm):
#     class Meta:
#         fields = ['dob']
#         widgets = {
#             'dob': forms.DateInput(attrs={'type': 'date'}),
#         }
#         model = Player
#         fields = '__all__'  # Use all fields from the Player model