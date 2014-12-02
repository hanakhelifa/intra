from django.contrib.auth.models import User
from django.test import TestCase
from tickets.models import Ticket


class TicketTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Lucas")
        User.objects.create(username="Emma")
        User.objects.create(username="Nathan")
        User.objects.create(username="Lea")

    def test_creation(self):
        user = User.objects.get(username="Emma")
        ticket = Ticket.create(title="Probleme de ticket", message="Il n'existe"
        " pas d'interface pour créer des tickets, comment faire ?", author=user)
        print(type(ticket), ticket, ticket.get_events())
        self.assertIsInstance(ticket, Ticket)
        events = ticket.get_events()
        self.assertEqual(len(events), 2)
