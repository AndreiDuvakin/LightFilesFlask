from functools import wraps

from quart import redirect, url_for
from quart_auth import current_user


def redirect_if_authenticated(endpoint: str = "files.files_page"):
    def decorator(view):
        @wraps(view)
        async def wrapper(*args, **kwargs):
            is_authenticated = await current_user.is_authenticated

            if is_authenticated:
                return redirect(url_for(endpoint))

            return await view(*args, **kwargs)

        return wrapper

    return decorator
