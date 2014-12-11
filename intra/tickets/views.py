from django.contrib.auth.decorators import login_required
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
