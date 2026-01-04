from django.contrib import admin
from . models import Customer, Student
# Register your models here.

admin.site.register(Student)
admin.site.register(Customer)