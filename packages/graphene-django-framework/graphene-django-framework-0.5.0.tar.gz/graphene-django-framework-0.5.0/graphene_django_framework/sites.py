from functools import partial
from typing import TYPE_CHECKING

import graphene
from django.contrib import admin
from graphene_django.types import DjangoObjectType
from graphene_django.views import GraphQLView

if TYPE_CHECKING:  # flake8: noqa
    from graphql.execution import ResolveInfo


class AdminSite(admin.AdminSite):
    graphql_url = 'api/'

    def get_urls(self):
        # from django.urls import path  # django 2.1
        from django.conf.urls import url
        urls = super().get_urls()
        urls += [url(self.graphql_url, self.admin_view(self.schema, cacheable=True), name='graphql'), ]
        return urls

    def get_query(self):
        query_class = [admin_class.get_query() for admin_class in self._registry.values()]

        class Query(graphene.ObjectType, *query_class):
            pass

        return Query

    def get_schema(self):
        return graphene.Schema(query=self.get_query())

    def schema(self, request, *args, **kwargs):
        return GraphQLView.as_view(graphiql=True, schema=self.get_schema())(request, *args, **kwargs)


class ModelAdmin(admin.ModelAdmin):
    def get_query(self):
        model_admin = self

        class Meta:
            model = self.model

        model_type = type('{}Type'.format(self.model.__name__),
                          (DjangoObjectType,),
                          {'Meta': Meta})

        # class UserType(DjangoObjectType):
        #     class Meta:
        #         model = self.model

        # class Query(object):
        user = graphene.Field(model_type, id=graphene.Int())
        all_users = graphene.List(model_type)

        def resolve_model(self, info: 'ResolveInfo', model=None, id=None, **kwargs):
            # self.get_object(request, unquote(object_id), to_field)
            return model.objects.get(pk=id)

        def resolve_model_plural(self, info: 'ResolveInfo', model=None, *args, **kwargs):
            queryset = model_admin.get_queryset(info.context)
            queryset, somthing = model_admin.get_search_results(info.context, queryset, kwargs.get('search', ''))
            return queryset

        # todo: slugify the names? make them configurable?
        name = self.model._meta.verbose_name.lower()
        name_plural = self.model._meta.verbose_name_plural.lower()

        return type('{}Query'.format(self.model.__name__),
                    (object,),
                    {name: graphene.Field(model_type, id=graphene.Int()),
                     name_plural: graphene.List(model_type, search=graphene.String()),
                     'resolve_{}'.format(name): partial(resolve_model, model=self.model),
                     'resolve_{}'.format(name_plural): partial(resolve_model_plural, model=self.model)})


site = AdminSite(name='Graph Admin')
