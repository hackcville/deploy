from django.contrib import admin
from .models import Dweet, User

# Register your models here.
admin.site.register(User)
admin.site.register(Dweet)
