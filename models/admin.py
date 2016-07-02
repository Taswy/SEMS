#coding=utf-8
from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)
    search_fields = ("username",)

	


admin.site.register(User,UserAdmin)
admin.site.register(AmmeterGroup)
admin.site.register(Ammeter)
admin.site.register(Charge)
admin.site.register(Account)
admin.site.register(Node)