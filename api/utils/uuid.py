import random
import string

from django.db import models

class OrgIDMixin(models.Model):
    # Sample of an ID generator - could be any string/number generator
    # For a 6-char field, this one yields 2.1 billion unique IDs
    def id_generator(self, size=18, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        while not self.id or self.__class__.objects.filter(id=self.id).exists():
            self.id = self.id_generator()

        super().save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)

    class Meta:
        abstract = True

