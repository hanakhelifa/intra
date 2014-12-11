from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from ticket.models import Ticket

@require_login
def pool(request):
    if not request.user.is_superuser:
        return HttpResponse("You don't have access")
