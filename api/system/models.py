from django.db import models

class Broadcast(models.Model):
    title = models.CharField(max_length=100)
    link_text = models.CharField(max_length=100)
    link_url = models.CharField(max_length=100)
    external = models.BooleanField(default=False)

    expired_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title