from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tickets.forms import TicketForm, MessageForm
from tickets.models import Ticket, Status

@login_required
def pool(request):
    if not request.user.is_superuser:
        return HttpResponse("You don't have access")
    tickets = (Ticket.objects
        .filter(last_status=Status.OPEN)
        .order_by('-last_event_date')
    )
    raise Http404

@login_required
def tickets_list(request):
    tickets = (Ticket.objects
        .filter(Q(last_assigned=request.user) | Q(author=request.user))
        .order_by('status', '-last_event_date')
    )
    return render(request, 'tickets/tickets_list.html', {'tickets': tickets})

@login_required
def create(request):
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST)
        form_message = MessageForm(request.POST)
    else:
        form_ticket = TicketForm()
        form_message = MessageForm()
    return render(
        request,
        'tickets/create.html',
        {
            'form_ticket': form_ticket,
            'form_message': form_message,
        }
    )
