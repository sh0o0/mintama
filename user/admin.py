from django.contrib import admin
from .models import User, Reference, Portfolio, Category


admin.site.register(User)
admin.site.register(Reference)
admin.site.register(Portfolio)
admin.site.register(Category)
