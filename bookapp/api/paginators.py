from rest_framework.pagination import PageNumberPagination

class WatchListPagination(PageNumberPagination):
    page_size = 4
    page_query_param = "record"
    page_size_query_param = "size"
    max_page_size = 10
    last_page_strings = ("end",)