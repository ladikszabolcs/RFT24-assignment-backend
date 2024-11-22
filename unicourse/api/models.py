from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

    # Avoid reverse accessor clashes by specifying related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    day_of_week = models.CharField(max_length=15)
    max_students = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name='lectures', limit_choices_to={'role': 'student'}, blank=True)

    def __str__(self):
        return self.title