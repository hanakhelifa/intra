from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

def beautify_users(users):
    result_list = list()
    for user in users:
        beautified_user = dict()
        beautified_user['uid'] = getattr(user, settings.ANNUAIRE_USER_UID)
        beautified_user['firstname'] = getattr(
            user,
            settings.ANNUAIRE_USER_FIRST_NAME
        )
        beautified_user['lastname'] = getattr(
            user,
            settings.ANNUAIRE_USER_LAST_NAME
        )
        beautified_user['profile_link'] = reverse(
            settings.ANNUAIRE_USER_PROFILE_VIEW,
            args=[
                getattr(user, arg)
                for arg in settings.ANNUAIRE_USER_PROFILE_VIEW_ARGS
            ]
        )
        result_list.append(beautified_user)
    return result_list

@login_required
def index(request):
    User = get_user_model()
    users = beautify_users(User.objects.all())
    context = {
        'users': users,
    }
    return render(request, 'annuaire/index.html', context)
