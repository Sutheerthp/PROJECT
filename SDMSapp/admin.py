# player_management/admin.py

from django.contrib import admin
from .models import Department,Programme, Student, Item, Stud_item 

admin.site.register(Department)
admin.site.register(Programme)
admin.site.register(Student)
admin.site.register(Item)
admin.site.register(Stud_item)
