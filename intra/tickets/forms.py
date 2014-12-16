from django import forms
from django.forms.models import inlineformset_factory
from tickets.models import Ticket, Message, Assign


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message', )


class AssignForm(forms.ModelForm):
    class Meta:
        model = Assign
        fields = ('assigned_to', )
