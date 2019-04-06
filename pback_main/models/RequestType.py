from django.db import models


class RequestType(models.Model):
    """Model representing a types of requests (e.g. to share your fields)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
