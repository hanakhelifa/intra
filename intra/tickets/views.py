from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
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
    raise Http404
