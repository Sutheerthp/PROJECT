from django.db import models
from django.core.validators import RegexValidator

class Department(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.dept_name)

class Programme(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=50)
    year_of_admission = models.IntegerField()
    admission_no = models.IntegerField()
    programme_id = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    uty_reg_no = models.CharField(max_length=50, unique = True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    place = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex='^\d{10}$', message='Phone number must be 10 to 15 digits')],
        default = 0
    )
    aadhar_number = models.CharField(
        max_length=12,
        validators=[RegexValidator(regex='^\d{12}$', message='Aadhaar number must be exactly 16 digits')],
        default = 0
    )
    dob = models.DateField(null =True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    DISTRICT = [
    ('ALAPPUZHA', 'Alappuzha'),
    ('ERNAKULAM', 'Ernakulam'),
    ('IDUKKI', 'Idukki'),
    ('KANNUR', 'Kannur'),
    ('KASARAGOD', 'Kasaragod'),
    ('KOLLAM', 'Kollam'),
    ('KOTTAYAM', 'Kottayam'),
    ('KOZHIKODE', 'Kozhikode'),
    ('MALAPPURAM', 'Malappuram'),
    ('PALAKKAD', 'Palakkad'),
    ('PATHANAMTHITTA', 'Pathanamthitta'),
    ('THIRUVANANTHAPURAM', 'Thiruvananthapuram'),
    ('THRISSUR', 'Thrissur'),
    ('WAYANAD', 'Wayanad'),
]

    district = models.CharField(max_length=50,  choices=DISTRICT, default='Active')
    pincode = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name} - {self.uty_reg_no}'

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    ITEM_TYPE = [
         ('SPORTS', 'SPORTS'),
         ('ATHLETICS', 'ATHLETICS'),
    ]
    item_type = models.CharField(max_length=50,  choices=ITEM_TYPE, default='Active')
    no_of_players = models.IntegerField()

    def __str__(self):
        return str(self.item_name)

class Stud_item(models.Model):
    stud = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    
    PLAYER_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    player_status = models.CharField(max_length=10, choices=PLAYER_STATUS_CHOICES, default='Active')
    
    UTY_SELECTION_STATUS_CHOICES = [
        ('Selected', 'Selected'),
        ('Not Selected', 'Not Selected'),
    ]
    uty_team_selection = models.CharField(max_length=20, choices=UTY_SELECTION_STATUS_CHOICES, default='Not Selected')
    
    position = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')

    def __str__(self):
        return f"{self.stud.name} - {self.item.item_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null= True)
    date = models.DateField()
    hour_1 = models.BooleanField(default=False)
    hour_2 = models.BooleanField(default=False)
    hour_3 = models.BooleanField(default=False)
    hour_4 = models.BooleanField(default=False)
    hour_5 = models.BooleanField(default=False)

    @property
    def hour_1_missed(self):
        return not self.hour_1

    @property
    def hour_2_missed(self):
        return not self.hour_2

    @property
    def hour_3_missed(self):
        return not self.hour_3

    @property
    def hour_4_missed(self):
        return not self.hour_4

    @property
    def hour_5_missed(self):
        return not self.hour_5

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class Picture(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    year = models.IntegerField()
    image = models.ImageField(upload_to='team_pictures')

    def __str__(self):
        return f"{self.team.name} - {self.year}"
    
class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    certificate_collected = models.BooleanField(default=False)
    year = models.IntegerField()
    programme_id = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    item_postion_types = [

        ('all_india_inter_university_1st', 'All India Inter University 1st'),
        ('all_india_inter_university_2nd', 'All India Inter University 2nd'),
        ('all_india_inter_university_3rd', 'All India Inter University 3rd'),
        ('all_india_inter_university_participation', 'All India Inter University participation'),
        ('south_zone_university_1st', 'South Zone University 1st'),
        ('south_zone_university_2nd', 'South Zone University 2nd'),
        ('south_zone_university_3rd', 'South Zone University 3rd'),
        ('south_zone_university_participation', 'South Zone University participation'),
        ('inter_collegiate_1st', 'Inter Collegiate 1st'),
        ('inter_collegiate_2nd', 'Inter Collegiate 2nd'),
        ('inter_collegiate_3rd', 'Inter Collegiate 3rd'),
        ('inter_collegiate_participation', 'Inter Collegiate participation'),
    ]
    item_postion = models.CharField(max_length=40, choices=item_postion_types, default='Not Selected')

    def __str__(self):
        return f"{self.student.name} - {self.item.item_name}"    