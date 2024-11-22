from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

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