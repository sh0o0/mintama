from django.contrib import admin
from .models import User, Reference, MainlyLearning, Portfolio


admin.site.register(User)
admin.site.register(Reference)
admin.site.register(MainlyLearning)
admin.site.register(Portfolio)