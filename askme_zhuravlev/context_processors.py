import names

from app.models import Profile, Tag


def top_tags(request):
    tag = Tag.objects.get_top_9()
    return {'top_tags': tag}


def top_users(request):
    users = Profile.objects.get_top_10()
    return {'top_users': users}

