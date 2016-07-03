#coding=utf-8
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","card_number","student_number","username","usage","default_money")
    search_fields = ("student_number","username","card_number",)
    list_filter = ["usage"]

@admin.register(AmmeterGroup)
class AmmeterGroupAdmin(admin.ModelAdmin):
    list_display = ("id","ammeterGroup_number","ammeterGroup_name","valid_number","sum_number",)
    search_fields = ("ammeterGroup_number","ammeterGroup_name",)

@admin.register(Ammeter)
class AmmeterAdmin(admin.ModelAdmin):
    list_display = ("id","ammeter_number","name","status","group",)
    search_fields = ("ammeter_number","name","group",)
    list_filter = ["status"]

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ("id","user","ammeter","status","start_time","end_time","overtime","message")
    search_fields = ("user__username","ammeter__ammeter_number",)
    list_filter = ["status"]

admin.site.register(Account)
admin.site.register(Node)