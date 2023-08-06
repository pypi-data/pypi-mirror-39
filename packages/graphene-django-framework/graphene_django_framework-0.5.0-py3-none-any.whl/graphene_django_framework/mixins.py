from functools import partial

import graphene
from graphene.types import List
from graphene_django.utils import maybe_queryset
from graphene_django.filter.utils import get_filtering_args_from_filterset
from django_filters.filterset import filterset_factory
from django.core.paginator import Paginator

from .paginator import PageType
from .utils import select_resolver


class PaginationMixin(object):
    """ Adds pagination functionality to a Field. """

    def __init__(self, _type,
                 per_page=graphene.Int(default_value=100),
                 orphans=graphene.Int(default_value=0),
                 # allow_empty_first_page  # todo: from paginator?
                 page=graphene.Int(default_value=1),
                 *args, **kwargs):
        kwargs.update(per_page=per_page,
                      orphans=orphans,
                      page=page)

        assert getattr(_type._meta, 'paginator', False), '{} needs to have a paginator.'.format(_type)
        self._type = _type._meta.paginator

        super(PaginationMixin, self).__init__(self._type, *args, **kwargs)

    @classmethod
    def page_resolver(cls, resolver, _type, root, info,
                      per_page: int = None,
                      page: int = None,
                      orphans: int = None,
                      **args):
        # per_page = args.pop('per_page')
        selected_resolver = select_resolver(resolver, _type.object_list.of_type, root)
        pager_ret = selected_resolver(root, info, **args)
        paginator = Paginator(maybe_queryset(pager_ret), per_page=per_page, orphans=orphans)
        page = paginator.page(page)
        return _type(
            page_info=PageType(paginator=paginator, page=page,
                               # object_count=paginator.count,
                               # num_pages=paginator.num_pages,
                               # page_range = paginator.page_range,
                               # has_next_page=page.has_next(),
                               # has_previous_page=page.has_previous(),
                               # has_other_pages=page.has_other_pages(),
                               # # next_page_number=page.next_page_number(),  # todo: catch error
                               # # previous_page_number=page.previous_page_number(),  # todo: catch error
                               # start_index=page.start_index(),
                               # end_index=page.end_index(),
                               ),
            object_list=page.object_list,
        )
        # return Paginator(num_pages=1)

    def get_resolver(self, parent_resolver):
        return partial(self.page_resolver, self.resolver or parent_resolver, self._type)


class FilterMixin(object):
    """ Adds filtering functionality to a Field. """

    def __init__(self, _type, filter_set_class=None, *args, **kwargs):
        # Passing in a custom FilterSet class
        if filter_set_class is not None:
            self._filter_set_class = filter_set_class

        else:
            # We may have gotten a List, so get the wrapped type's _meta if so
            type_meta = _type.of_type._meta if isinstance(_type, List) else _type._meta

            # filter_fields specified in type's meta
            if getattr(type_meta, 'filter_fields', False):
                self._filter_set_class = filterset_factory(type_meta.model, fields=type_meta.filter_fields)

            else:
                raise NotImplementedError('No filters found. '
                                          'Specify filter_fields through the type\'s Meta, '
                                          'or pass a FilterSet to the Field.')

        filter_args = get_filtering_args_from_filterset(self._filter_set_class, _type)
        kwargs.update(filter_args)

        super(FilterMixin, self).__init__(_type, *args, **kwargs)

    @classmethod
    def filter_resolver(cls, resolver, _type, filter_set_class, root, info, **args):
        selected_resolver = select_resolver(resolver, _type, root)
        parent_ret = selected_resolver(root, info, **args)

        # TODO: Get only filtering arguments from args
        filter_set = filter_set_class(data=args, queryset=maybe_queryset(parent_ret), request=info.context)

        return filter_set.qs

    def get_resolver(self, parent_resolver):
        return partial(self.filter_resolver, self.resolver or parent_resolver, self._type, self._filter_set_class)
