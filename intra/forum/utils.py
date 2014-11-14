from django.conf import settings
from django.core.urlresolvers import reverse

def custom_set(query_set):
    for entry in query_set:
        author = {}
        author['username'] = entry.author.get_username()
        author['profile_url'] = reverse(
            settings.FORUM_USER_PROFILE_VIEW,
            args=[
                getattr(entry.author, arg)
                for arg in settings.FORUM_USER_PROFILE_VIEW_ARGS
            ]
        )
        if hasattr(settings, 'FORUM_AVATAR_FIELD'):
            author['avatar'] = getattr(
                entry.author,
                settings.FORUM_AVATAR_FIELD
            )
        entry.clean_author = author
    return query_set
