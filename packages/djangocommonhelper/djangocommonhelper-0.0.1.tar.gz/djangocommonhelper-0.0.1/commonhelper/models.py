from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract model that includes a modified and a created DateTimeField
    To use in your own Model:
    class MyModel(TimeStampedModel):
        Fields go here
    """
    modified = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract=True
