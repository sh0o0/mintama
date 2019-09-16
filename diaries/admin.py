from django.contrib import admin
    
from .models import Diary, Section

admin.site.register(Diary)
admin.site.register(Section)