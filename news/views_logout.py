from django.contrib.auth.views import LogoutView


class CustomLogout(LogoutView):
    """
    Custom logout view.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
