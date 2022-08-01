from django.contrib.auth.models import AbstractUser, Group

from django.db import models

from org.models import Org

class User(AbstractUser):
    org = models.ManyToManyField(Org)