from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid as uuid_lib

from .constant import RESIDENCE_CHOICIES, CRACK_LEVEL_CHOICIES, REFERENCE_EVALUATION_CHOICIES, GENDER_CHOICIES


class Category(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False)

    gender = models.CharField(
        max_length=6,
        blank=True,
        choices=GENDER_CHOICIES
    )
    residence = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=RESIDENCE_CHOICIES,
    )
    introduction = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    icon = models.ImageField(
        upload_to='img',
        blank=True,
        null=True,
    )
    learning_started_date = models.DateField(
        blank=True,
        null=True,
    )
    crack_level = models.IntegerField(
        default=1,
        choices=CRACK_LEVEL_CHOICIES,
    )

    mainly_learning = models.ManyToManyField(
        Category,
        related_name='users',
        blank=True
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    #TODO:Will implement the following
    # diaries_num = models.IntegerField(
    #     blank=True,
    #     null=True,
    # )
    # saved_diaries = models.ManyToManyField(
    #     Diary,
    #     blank=True,
    #     null=True,
    # )
    # good_diaries = models.ManyToManyField(
    #     Diary,
    #     blank=True,
    #     null=True,
    # )
    # praised_diaries = models.ManyToManyField(
    #     Diary,
    #     blank=True,
    #     null=True,
    # )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # @delete_previous_file
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    # @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        return super().delete(using=None, keep_parents=False)

    def __str__(self):
        return self.username


class Reference(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='references',
    )
    title = models.CharField(
        max_length=100,
    )
    evaluation = models.FloatField(
        choices=REFERENCE_EVALUATION_CHOICIES,
        blank=True,
        null=True,
    )
    content = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    link = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{}(user: {})'.format(self.title, self.user)


class Portfolio(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='portfolios'
    )
    title = models.CharField(
        max_length=100,
    )
    content = models.TextField()

    link = models.URLField()

    def __str__(self):
        return '{}(user: {})'.format(self.title, self.user)