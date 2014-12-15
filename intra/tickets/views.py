from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from tickets.forms import TicketForm, MessageForm, AssignForm
from tickets.models import Ticket, Status

@login_required
def pool(request):
    if not request.user.is_superuser:
        return HttpResponse("You don't have access")
    tickets_open = (Ticket.objects
        .filter(last_status=Status.OPEN)
        .order_by('-last_event_date')
    )
    tickets_close = (Ticket.objects
            .filter(last_status=Status.CLOSE)
        .order_by('-last_event_date')
    )
    return render(request, 'tickets/pool.html',
        {
            'opened_tickets': tickets_open,
            'closed_tickets': tickets_close
        }
    )

@login_required
def tickets_list(request):
    tickets = (Ticket.objects
        .filter(
            (Q(last_assigned=request.user) & ~Q(author=request.user))
            | Q(author=request.user)
        )
        .order_by('last_status', '-last_event_date')
    )
    return render(request, 'tickets/tickets_list.html', {'tickets': tickets})

@login_required
def create(request):
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST)
        form_message = MessageForm(request.POST)
        if form_ticket.is_valid() and form_message.is_valid():
            ticket = Ticket.create(
                title=form_ticket.cleaned_data['title'],
                message=form_message.cleaned_data['message'],
                author=request.user
            )
            return HttpResponseRedirect(reverse(
                'tickets:view',
                args=[ticket.pk, ]
            ))
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
    if (
        request.user != ticket.author
        and request.user != ticket.last_assigned
        and not request.user.is_superuser
    ):
        return Http404
    assign_form = None
    if request.method == "POST":
        if 'open' in request.POST:
            ticket.open(request.user)
            form = MessageForm()
            if request.user.is_superuser:
                assign_form = AssignForm()
        else:
            form = MessageForm(request.POST)
            if request.user.is_superuser:
                assign_form = AssignForm(request.POST)
            if form.is_valid() or assign_form.is_valid():
                if form.is_valid():
                    ticket.add_message(
                        author=request.user,
                        message=form.cleaned_data['message']
                    )
                    form = MessageForm()
                if assign_form.is_valid():
                    assign = ticket.assign(
                        author=request.user,
                        to=assign_form.cleaned_data['assigned_to']
                    )
            form = MessageForm()
            if request.user.is_superuser:
                assign_form = AssignForm()
        if 'close' in request.POST:
            ticket.close(request.user)
            form = MessageForm()
            if request.user.is_superuser:
                assign_form = AssignForm()
    else:
        form = MessageForm()
        if request.user.is_superuser:
            assign_form = AssignForm()
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
