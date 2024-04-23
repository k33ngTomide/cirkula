from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CirkulaUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        app_label = 'user'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cirkula_user_groups',  # Unique related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cirkula_user_permissions',  # Unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


class Meta:
    permissions = [
        ("view_cirkulauser", "Can view CirkulaUser"),
    ]


