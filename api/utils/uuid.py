import random
import string

from django.db import models

class OrgIDMixin(models.Model):
    # Sample of an ID generator - could be any string/number generator
    # For a 6-char field, this one yields 2.1 billion unique IDs
    def id_generator(self, size=18, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.id:
            generated_id = self.id_generator()
            while self.__class__.objects.filter(id=self.id).exists():
                generated_id = self.id_generator()
            
            self.id = generated_id

        super().save(*args, **kwargs)

    id = models.CharField(primary_key=True, max_length=256, blank=True, unique=True)

    class Meta:
        abstract = True

