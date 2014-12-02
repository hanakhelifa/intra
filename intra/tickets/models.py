from django.conf import settings
from django.db import models
from itertools import chain


class Message(models.Model):
    ticket = models.ForeignKey('Ticket')
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
    status = models.IntegerField(choices=Status, default=OPEN)
    date = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_status(self):
        status = self.status_set.all().order_by('id').first()
        if status is None:
            return Status.OPEN
        return status

    def get_assigned(self):
        return self.assign_set.all().order_by('id').first()

    def get_events(self):
        messages = self.message_set.all().order_by('date')
        assign = self.assign_set.all().order_by('date')
        status = self.status_set.all().order_by('date')
        event_list = chain(messages, assign, status)
        event_list = sorted(event_list, key=lambda elem: elem.date)
        return event_list

    def create(title, message, author):
        ticket = Ticket(title=title, author=author);
        ticket.save();
        ticket.status_set.create(author=author, status=Status.OPEN)
        ticket.message_set.create(author=author, message=message)
        return ticket
