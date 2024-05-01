from django.http import HttpResponseForbidden


class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/rosetta/' in request.path.lower() and not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to access this page.")

        response = self.get_response(request)
        return response
