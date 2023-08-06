
import graphene
from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions
# todo: is this the best way to do this?
# from .converter import * << this line should be below:
from graphene_django.utils import maybe_queryset

from .converter import convert_django_field
from .paginator import PaginatorType


def _import_convert_django_field():
    """
    This is only here so the import optimizer do not remove it.
    todo: is there a better way?
    """
    return convert_django_field


class ModelObjectType(DjangoObjectType):
    """
    Overloading the DjangoObjectType class in order to add the Paginator class to the _meta.
    """

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, perms=None, **options):
        if not _meta:
            _meta = DjangoObjectTypeOptions(cls)

        PageMeta = {'description': cls.__name__}
        PageClass = type('{}Paginator'.format(cls.__name__), (PaginatorType,), {
            'Meta': PageMeta,
            'object_list': graphene.List(cls)})
        _meta.paginator = PageClass
        _meta.perms = perms

        super(ModelObjectType, cls).__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def get_qs(cls, resolver, root, info, **args):
        """ Default resolver when resolving a QuerySet at the root level.

            :param resolver
            :param root
            :param info
        """
        return maybe_queryset(resolver(root, info, **args))

    @classmethod
    def get_model_instance(cls, resolver, root, info, id=None, **args):
        """ Default resolver when resolving a Model instance. """
        return cls._meta.model._default_manager.get(id=id)

    @classmethod
    def get_perms(cls):
        """ Return Permissions to enforce when using the default resolve on the type. """
        perms = getattr(cls._meta, 'perms', None)

        # We allow perms to be None, which means "No permission required".
        # Setting perms to an empty tuple means "Default permissions required".
        if perms is not None and not perms:
            # Default permissions are of the form: '<app_label>.view_<model_name>'
            perms = ('{}.view_{}'.format(cls._meta.model._meta.app_label, cls._meta.model._meta.model_name), )

        if isinstance(perms, str):
            # Ensure that we return a tuple when a programmer specifies a single Permission string
            perms = (perms, )

        return perms
