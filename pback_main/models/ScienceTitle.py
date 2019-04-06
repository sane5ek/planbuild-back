from django.db import models


class ScienceTitle(models.Model):
    """Model representing a types of science titles (e.g. )"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
