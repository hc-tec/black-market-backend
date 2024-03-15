from rest_framework.pagination import PageNumberPagination


class GoodsPagination(PageNumberPagination):

    page_size = 4

class ThreadPagination(PageNumberPagination):

    page_size = 4

class GenericPagination(PageNumberPagination):

    page_size = 5

class TopicPagination(PageNumberPagination):

    page_size = 8

class ThreadCommentPagination(PageNumberPagination):

    page_size = 5

