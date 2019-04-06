from django.db import models
from django.utils import timezone


class Request(models.Model):
    sender = models.ForeignKey('pback_auth.User', related_name='Request_sender', null=False, default=0,
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey('pback_auth.User', related_name='Request_receiver', null=False, default=0,
                                 on_delete=models.CASCADE)
    type = models.ForeignKey('pback_main.RequestType', null=False, default=0, on_delete=models.CASCADE)
    create_date = models.DateTimeField('Date of setting sender request', null=False, default=timezone.now)
    answer_date = models.DateTimeField('Date of getting receiver answer', null=True, default=None)
    result = models.ForeignKey('pback_main.RequestResultType', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return "From {0} to {1} type {2}".format(self.sender, self.receiver, self.type)
