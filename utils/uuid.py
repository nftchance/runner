import random
import string

# Sample of an ID generator - could be any string/number generator
# For a 6-char field, this one yields 2.1 billion unique IDs
def id_generator(size=18, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))