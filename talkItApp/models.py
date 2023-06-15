from enum import Enum

from django.db import models


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    apiCode = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in Gender])
    prompt = models.CharField(max_length=1024, blank=True, null=True)
    last_msgs = models.CharField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
