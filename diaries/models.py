from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from mintama.get_outer_model import get_category_model, get_reference_model


User = get_user_model()
Category = get_category_model()
Reference = get_reference_model()


class Diary(models.Model):
    user = models.ForeignKey(
        User,
        related_name='diaries',
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
    diary = models.ForeignKey(
        Diary,
        related_name='diary_sections',
        on_delete=models.CASCADE
    )
    heading = models.CharField(max_length=50)
    content = models.TextField()
    references = models.ManyToManyField(
        Reference,
        related_name='reference_sections',
        blank=True,
    )
    
    def __str__(self):
        return '{}({})'.format(self.heading, self.title)