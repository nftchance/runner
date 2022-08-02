from django.contrib.auth.models import AbstractUser, Group

from django.db import models

from org.models import OrgRelationship

class User(AbstractUser):
    org_relationships = models.ManyToManyField(OrgRelationship)