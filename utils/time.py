import django
import math


def seconds_until(time):
    if not time:
        return None
    return math.floor(time.timestamp() - django.utils.timezone.now().timestamp())
