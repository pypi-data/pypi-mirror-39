import string
import random


def unique_slug(Model, length=8):
    """
    Assumes that there is a field in the model called "Slug." This will make sure
    that a unique slug of length is created, made up of uppercase letters and digits
    """
    slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    while Model.objects.filter(slug=slug):
        slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    return slug
