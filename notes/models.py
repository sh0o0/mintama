from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Category, Reference

User = get_user_model()


class Note(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notes',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=50)
    written_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Section(models.Model):
    categories = models.ManyToManyField(
        Category,
        related_name='category_sections',
        blank=True,
    )
    note = models.ForeignKey(
        Note,
        related_name='note_sections',
        on_delete=models.CASCADE
    )
    heading = models.CharField(
        max_length=50)
    content = models.TextField(
        blank=True,
    )
    references = models.ManyToManyField(
        Reference,
        related_name='reference_sections',
        blank=True,
    )
        
    def __str__(self):
        return self.heading