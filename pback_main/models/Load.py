from django.db import models


class Load(models.Model):
    """Model representing a types of loads (e.g. 1_1M)"""
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
