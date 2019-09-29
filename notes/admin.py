from django.contrib import admin
    
from .models import Note, Section

admin.site.register(Note)
admin.site.register(Section)