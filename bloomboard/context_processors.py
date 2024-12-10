from .models import *

def user_profile(request):
    """Add the authenticated user's BBProfile to the template context."""
    result = {}
    if request.user.is_authenticated :
        try:
            bbprofile = BBProfile.objects.get(user=request.user)
            first_name = bbprofile.get_first_name()
            result = {'bbprofile': bbprofile, 'first_name': first_name}
        except BBProfile.DoesNotExist:
            bbprofile = None
    return result
        