
from django.db import models
from graphene import Dynamic, Int
from graphene_django.converter import convert_django_field
from graphene_django.fields import DjangoConnectionField, DjangoListField


@convert_django_field.register(models.ManyToManyField)
@convert_django_field.register(models.ManyToManyRel)
@convert_django_field.register(models.ManyToOneRel)
def convert_field_to_list_or_connection(field, registry=None):
    model = field.related_model

    def dynamic_type():
        _type = registry.get_type_for_model(model)
        if not _type:
            return

        # If there is a paginator change to a PageList
        if getattr(_type._meta, 'paginator', None):
            from graphene_django_framework.fields import ModelPageListField  # todo: can this go to the top?

            return ModelPageListField(_type)

        # If there is a connection, we should transform the field
        # into a DjangoConnectionField
        if _type._meta.connection:  # pragma: no cover
            # Use a DjangoFilterConnectionField if there are
            # defined filter_fields in the DjangoObjectType Meta
            if _type._meta.filter_fields:
                from graphene_django.filter.fields import DjangoFilterConnectionField

                return DjangoFilterConnectionField(_type)

            return DjangoConnectionField(_type)

        return DjangoListField(_type)  # pragma: no cover

    return Dynamic(dynamic_type)
