from django.contrib.auth.models import User
from django.test import TestCase
from tickets.models import Ticket


class TicketTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Lucas")
        User.objects.create(username="Emma")
        User.objects.create(username="Nathan")
        User.objects.create(username="Lea")

    def TestCreation(self):
        Ticket.create()
