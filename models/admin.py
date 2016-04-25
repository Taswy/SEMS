#coding=utf-8
from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","student_number")
    search_fields = ("student_number","username")




admin.site.register(User,UserAdmin)
admin.site.register(Ammeter)
admin.site.register(Charge)
admin.site.register(Manager)
admin.site.register(Account)