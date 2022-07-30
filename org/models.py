from django.db import models

from utils.uuid import id_generator

class Org(models.Model):
    def save(self, *args, **kwargs):
        while not self.id or Org.objects.filter(id=self.id).exists():
            self.id = id_generator()

        super(Org, self).save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=6, blank=True, unique=True)

    name = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]