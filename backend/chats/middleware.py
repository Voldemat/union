from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    try:
        return get_user_model().objects.get(id = user_id)
    except get_user_model().DoesNotExist:
        return None

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        print(scope)

        return await self.app(scope, receive, send)