from .models import BBProfile

def user_profile(request):
    """Add the authenticated user's BBProfile to the template context."""
    if request.user.is_authenticated:
        try:
            bbprofile = BBProfile.objects.get(user=request.user)
            first_name = bbprofile.get_first_name()
        except BBProfile.DoesNotExist:
            bbprofile = None
    else:
        bbprofile = None
    return {'bbprofile': bbprofile, 'first_name': first_name}