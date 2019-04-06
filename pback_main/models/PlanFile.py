from django.db import models


class PlanFile(models.Model):
    file = models.FileField(upload_to='files/plans/%Y/%m/%d')
    owner = models.ForeignKey('pback_auth.User', null=True, default=None, on_delete=models.SET_NULL)
