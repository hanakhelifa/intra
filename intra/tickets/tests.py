from django.contrib.auth.models import User
from django.test import TestCase
from tickets.models import Ticket, Status, Message


class TicketTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Lucas")
        User.objects.create(username="Emma")
        User.objects.create(username="Nathan")
        User.objects.create(username="Lea")

    def test_creation(self):
        """A ticket require title, message and author to be created"""
        user = User.objects.get(username="Emma")
        ticket = Ticket.create(title="Probleme de ticket", message="Il n'existe"
        " pas d'interface pour créer des tickets, comment faire ?", author=user)
        self.assertIsInstance(ticket, Ticket)

    def test_events(self):
        """The event list must be sorted by date (Or order of creation)"""
        user = User.objects.get(username="Emma")
        ticket = Ticket.create(title="Probleme de ticket", message="Il n'existe"
        " pas d'interface pour créer des tickets, comment faire ?", author=user)
        self.assertIsInstance(ticket, Ticket)
        events = ticket.get_events()
        self.assertEqual(len(events), 2)
        self.assertIsInstance(events[0], Status)
        self.assertEqual(events[0].status, Status.OPEN)
        self.assertIsInstance(events[1], Message)
        self.assertEqual(events[1].message, "Il n'existe pas d'interface"
            " pour créer des tickets, comment faire ?")
