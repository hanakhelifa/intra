from django.conf import settings
from django.db import models
from itertools import chain


class Message(models.Model):
    def __str__(self):
        return self.message

    ticket = models.ForeignKey('Ticket')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Assign(models.Model):
    def __str__(self):
        return ('Assigned to ' + self.assigned_to.get_username()
            + ' by ' + self.author.get_username()
        )

    ticket = models.ForeignKey('Ticket')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_by'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_to'
    )
    date = models.DateTimeField(auto_now=True)


class Status(models.Model):
    OPEN = 0
    CLOSE = 1

    Status = (
        (OPEN, 'Opened'),
        (CLOSE, 'Closed'),
    )

    def __str__(self):
        return self.Status[self.status][1] + ' by ' + self.author.get_username()

    ticket = models.ForeignKey('Ticket')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(choices=Status, default=OPEN)
    date = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

    def get_status(self):
        status = self.status_set.all().order_by('-id').first()
        if status is None:
            return Status.OPEN
        return status.status

    def get_assigned(self):
        assign = self.assign_set.all().order_by('-id').first()
        if assign is None:
            return None
        return assign.assigned_to

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

    def add_message(self, author, message):
        if not (self.get_status() is Status.CLOSE):
            return self.message_set.create(author=author, message=message)
        return None

    def close(self, author):
        if not (self.get_status() is Status.CLOSE):
            return self.status_set.create(author=author, status=Status.CLOSE)
        return None

    def open(self, author):
        if not (self.get_status() is Status.OPEN):
            return self.status_set.create(author=author, status=Status.OPEN)
        return None

    def assign(self, author, to):
        if not (self.get_assigned() is to):
            return self.assign_set.create(author=author, assigned_to=to)
        return None
