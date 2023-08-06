from functools import partial

from graphene.types.resolver import get_default_resolver

from .decorators import needs_permission


def select_resolver(resolver, _type, root):
    """ Select the resolver to use when retrieving a list of objects.

        :param resolver: partial object or function
        :param _type: ModelObjectType
        :param root
    """
    resolver_func = resolver.func if isinstance(resolver, partial) else resolver
    type_perms = _type.get_perms()
    default_resolver = get_default_resolver()

    selected_resolver = resolver
    if root is None:
        # We don't have a parent element

        if resolver_func is default_resolver:
            # If the resolver is the default attr_resolver, use the get_qs() resolver defined on the type
            selected_resolver = partial(_type.get_qs, resolver)

    # TODO: Enforce type permissions on all resolvers instead of just the default resolver
    if resolver_func is default_resolver and type_perms is not None:
        # Enforce permissions defined on the type
        selected_resolver = needs_permission(*type_perms)(selected_resolver)

    return selected_resolver
