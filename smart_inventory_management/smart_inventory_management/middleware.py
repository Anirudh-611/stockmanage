from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. If user is authenticated, let them proceed.
        if request.user.is_authenticated:
            return self.get_response(request)

        # 2. Get the current URL path.
        path = request.path_info

        # 3. Define the list of paths that do not require authentication.
        exempt_paths = [
            '/login/',
            '/signup/',
            '/products/',
            '/dashboard/',
            '/',
        ]

        # 4. Check if the path is exempt, starts with admin, or starts with static URL.
        static_url = getattr(settings, 'STATIC_URL', '/static/')
        
        is_exempt = (
            path in exempt_paths or
            path.startswith('/admin/') or
            (static_url and path.startswith(static_url))
        )

        if not is_exempt:
            return redirect('/login/')

        return self.get_response(request)
    