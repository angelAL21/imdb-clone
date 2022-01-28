from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10 #10 elements on each page.
    last_page_strings = 'end'

class WatchListOffsetPag(LimitOffsetPagination):
    pass
    default_limit = 5
    max_limit = 10 
    limit_query_param = 'limit'
    offset_query_param = 'start'
    
class WatchCPagination(CursorPagination):
    page_size = 5
    ordering = 'created' 
    cursor_query_param = 'record'