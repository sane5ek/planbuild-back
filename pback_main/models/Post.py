from django.db import models


class Post(models.Model):
    """Model representing of a types posts (e.g. Teacher)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
