import graphene
from django.core.paginator import InvalidPage


class BasePageType(graphene.ObjectType):
    def __init__(self, *args, **kwargs):
        super(BasePageType, self).__init__(*args, **kwargs)

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        super(BasePageType, cls).__init_subclass_with_meta__(**options)


class PageType(BasePageType):
    def __init__(self, paginator=None, page=None, *args, **kwargs):
        self.paginator = paginator
        self.page = page
        super(BasePageType, self).__init__(*args, **kwargs)

    object_count = graphene.Int()  # conflicts with count attr
    # num_pages = graphene.Int(abs=graphene.Boolean(default_value=False))
    num_pages = graphene.Int()
    page_range = graphene.List(graphene.Int)
    has_next = graphene.Boolean()
    has_previous = graphene.Boolean()
    has_other_pages = graphene.Boolean()
    next_page_number = graphene.Int()
    previous_page_number = graphene.Int()
    start_index = graphene.Int()
    end_index = graphene.Int()

    def resolve_object_count(self, info):
        return self.paginator.count

    def resolve_num_pages(self, info):
        return self.paginator.num_pages

    def resolve_page_range(self, info):
        return self.paginator.page_range

    def resolve_has_next(self, info):
        return self.page.has_next()

    def resolve_has_previous(self, info):
        return self.page.has_previous()

    def resolve_has_other_pages(self, info):
        return self.page.has_other_pages()

    def resolve_next_page_number(self, info):
        try:
            return self.page.next_page_number()
        except InvalidPage:
            pass
        return None

    def resolve_previous_page_number(self, info):
        try:
            return self.page.previous_page_number()
        except InvalidPage:
            pass
        return None

    def resolve_start_index(self, info):
        return self.page.start_index()

    def resolve_end_index(self, info):
        return self.page.end_index()


class BasePaginatorType(graphene.ObjectType):
    def __init__(self, *args, **kwargs):
        # self.page_info = page_info
        # kwargs.update(page_info=page_info)
        super(BasePaginatorType, self).__init__(*args, **kwargs)

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        super(BasePaginatorType, cls).__init_subclass_with_meta__(**options)


class PaginatorType(graphene.ObjectType):
    page_info = graphene.Field(PageType)

    # object_list = graphene.List(UserType)  # dynamically created with PageList

    class Meta:
        description = 'This is a Paginator'  # todo: remove
