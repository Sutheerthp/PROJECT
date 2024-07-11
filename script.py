import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings')
django.setup()

# Import your models
from SDMSapp.models import Student, Programme

# Define dummy data
dummy_students = [
    {
        'name': 'John Doe',
        'year_of_admission': 2022,
        'admission_no': 1234,
        'programme_id': Programme.objects.get(pk=1),  # Assuming Programme with ID 1 exists
        'uty_reg_no': 'UTY123',
        'place': 'Some Place',
        'city': 'Some City',
        'district': 'Some District',
        'pincode': '12345'
    },
    # Add more dummy student data as needed
]

# Add dummy data to the Student model
for student_data in dummy_students:
    student = Student.objects.create(**student_data)
    print(f"Created student: {student.name}")
