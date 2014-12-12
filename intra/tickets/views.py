from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from tickets.forms import TicketForm, MessageForm, AssignForm
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
        if form_ticket.is_valid() and form_message.is_valid():
            Ticket.create(
                title=form_ticket.cleaned_data['title'],
                message=form_message.cleaned_data['message'],
                author=request.user
            )
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

@login_required
def view(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = MessageForm()
    if request.user.is_superuser:
        assign_form = AssignForm()
    else:
        assign_form = None
    events = ticket.get_events()
    return render(
        request,
        'tickets/view.html',
        {
            'ticket': ticket,
            'ticket_id': ticket_id,
            'events': events,
            'form': form,
            'assign_form': assign_form,
            'Status': Status,
        }
    )
