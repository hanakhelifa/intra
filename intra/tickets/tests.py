from django.contrib.auth.models import User
from django.test import TestCase
from tickets.models import Ticket, Status, Message, Assign


class TicketTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Lucas")
        User.objects.create(username="Emma")
        User.objects.create(username="Nathan")
        User.objects.create(username="Lea")

    def test_ticket_creation(self):
        """A ticket require title, message and author to be created"""
        user = User.objects.get(username="Emma")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=user
        )
        self.assertIsInstance(ticket, Ticket)

    def test_ticket_creation_events(self):
        """At ticket creation, the ticket status must be set to OPEN and a"""
        """ message must be created."""
        user = User.objects.get(username="Emma")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=user
        )
        self.assertEqual(ticket.status_set.all().count(), 1)
        status = ticket.status_set.get()
        self.assertEqual(status.status, Status.OPEN)
        self.assertEqual(ticket.message_set.all().count(), 1)
        message = ticket.message_set.get()
        self.assertEqual(message.message, "Il n'existe pas d'interface"
            " pour créer des tickets, comment faire ?")
        self.assertEqual(ticket.assign_set.all().count(), 0)

    def test_ticket_close_1(self):
        """Closing an opened ticket may succed"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        status = ticket.close(author=lucas)
        self.assertIsInstance(status, Status)
        self.assertEqual(status.status, Status.CLOSE)

    def test_ticket_close_2(self):
        """Closing a closed ticket may fail"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        ticket.close(author=lucas)
        self.assertEqual(ticket.close(author=lucas), None)

    def test_ticket_open_1(self):
        """Opening a closed ticket may succed"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        ticket.close(author=lucas)
        status = ticket.open(author=lucas)
        self.assertIsInstance(status, Status)
        self.assertEqual(status.status, Status.OPEN)

    def test_ticket_open_2(self):
        """Opening a opened ticket may fail"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        self.assertEqual(ticket.open(author=lucas), None)

    def test_ticket_add_message_1(self):
        """Adding a message to an opened ticket may succed"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        message = ticket.add_message(lucas, "OKTAMER")
        self.assertIsInstance(message, Message)
        self.assertEqual(message.author, lucas)
        self.assertEqual(message.message, "OKTAMER")

    def test_ticket_add_message_2(self):
        """Adding a message to a closed ticket may fail"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        ticket.close(author=emma)
        message = ticket.add_message(lucas, "OKTAMER")
        self.assertEqual(message, None)

    def test_ticket_assign_1(self):
        """Assign a ticket to a different user than the actual assigned user"""
        """ may succed"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        lea = User.objects.get(username="Lea")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        assign = ticket.assign(author=lucas, to=lea)
        self.assertIsInstance(assign, Assign)
        self.assertEqual(assign.author, lucas)
        self.assertEqual(assign.assigned_to, lea)

    def test_ticket_assign_2(self):
        """Assign a ticket to the same user than the actual assigned user"""
        """ may fail"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        lea = User.objects.get(username="Lea")
        nathan = User.objects.get(username="Nathan")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        ticket.assign(author=nathan, to=lea)
        self.assertEqual(ticket.assign(author=lucas, to=lea), None)

    def test_ticket_events(self):
        """The event list must be sorted by date (Or order of creation)"""
        emma = User.objects.get(username="Emma")
        lucas = User.objects.get(username="Lucas")
        nathan = User.objects.get(username="Nathan")
        ticket = Ticket.create(
            title="Probleme de ticket",
            message="Il n'existe pas d'interface pour créer des tickets,"
                " comment faire ?",
            author=emma
        )
        ticket.add_message(
            lucas,
            "J'assigne ce ticket a notre developpeur front-end"
        )
        ticket.assign(lucas, nathan)
        ticket.add_message(nathan, "La section de creation de ticket a ete mise"
            " en ligne.")
        ticket.close(nathan)
        ticket.open(emma)
        ticket.add_message(emma, "Le bouton \"Envoyer\" ne fonctionne pas")

        events = ticket.get_events()
        self.assertEqual(len(events), 8)

        self.assertIsInstance(events[0], Status)
        self.assertEqual(events[0].status, Status.OPEN)

        self.assertIsInstance(events[1], Message)
        self.assertEqual(events[1].message, "Il n'existe pas d'interface"
            " pour créer des tickets, comment faire ?")

        self.assertIsInstance(events[2], Message)
        self.assertEqual(events[2].message, "J'assigne ce ticket a notre"
            " developpeur front-end")

        self.assertIsInstance(events[3], Assign)
        self.assertEqual(events[3].assigned_to, nathan)

        self.assertIsInstance(events[4], Message)
        self.assertEqual(events[4].message, "La section de creation de ticket"
            " a ete mise en ligne.")

        self.assertIsInstance(events[5], Status)
        self.assertEqual(events[5].status, Status.CLOSE)

        self.assertIsInstance(events[6], Status)
        self.assertEqual(events[6].status, Status.OPEN)

        self.assertIsInstance(events[7], Message)
        self.assertEqual(events[7].message, "Le bouton \"Envoyer\" ne"
            " fonctionne pas")
