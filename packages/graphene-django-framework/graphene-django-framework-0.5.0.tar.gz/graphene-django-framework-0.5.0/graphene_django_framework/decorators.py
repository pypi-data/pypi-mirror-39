import functools

from django.core.exceptions import PermissionDenied


def only_allow(superuser=False, staff=False):
    """ Handle access to GraphQL endpoints to certain Users.

        Use on resolver functions, either at the Query level or ObjectType level.
    """
    def decorator_wrapper(func):

        @functools.wraps(func)
        def wrapper(cls, info, **kwargs):

            allow_list = []

            if staff:
                allow_list.append(info.context.user.is_staff)

            if superuser:
                allow_list.append(info.context.user.is_superuser)

            if not any(allow_list):
                raise PermissionDenied('You are not allowed to do that.')

            return func(cls, info, **kwargs)

        return wrapper

    return decorator_wrapper


def needs_permission(*permissions):
    """ Handle permissions required to query GraphQL endpoints.

        Use on resolver functions, either at the Query or ObjectType level.
    """
    def decorator_wrapper(func):

        @functools.wraps(func)
        def wrapper(cls, info, **kwargs):

            if info.context.user.has_perms(permissions):
                return func(cls, info, **kwargs)

            raise PermissionDenied('You do not have permission to do that.')

        return wrapper

    return decorator_wrapper


def needs_module_permissions(app_label):
    """ Handle module permissions required to query GraphQL endpoints (i.e. 'if perms.auth: .... ').

        Use on resolver functions, either at the Query or ObjectType level.
    """
    def decorator_wrapper(func):

        @functools.wraps(func)
        def wrapper(cls, info, **kwargs):

            # If the User has any of the permissions in the given module, they can access the query
            if info.context.user.has_module_perms(app_label):
                return func(cls, info, **kwargs)

            raise PermissionDenied('You do not have permission to do that.')

        return wrapper

    return decorator_wrapper
