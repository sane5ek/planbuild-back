from django.db import models


class ScienceDegree(models.Model):
    """Model representing a types of science degrees (e.g. )"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
