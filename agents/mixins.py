from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganizerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated or is a organizer or not."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect("leads:leads-list")
        return super().dispatch(request, *args, **kwargs)