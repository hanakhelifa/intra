from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Assign(models.Model):
    ticket = models.ForeignKey('Ticket')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now=True)


class Status(models.Model):
    OPEN = 0
    CLOSE = 1

    Status = (
        (OPEN, 'Opened'),
        (CLOSE, 'Closed'),
    )

    ticket = models.ForeignKey('Ticket')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.ChoiceField(choices=Status, default=OPEN)
