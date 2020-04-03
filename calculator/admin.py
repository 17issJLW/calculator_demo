from django.contrib import admin

# Register your models here.
from calculator.models import History, MyUser

admin.site.register(History)
admin.site.register(MyUser)