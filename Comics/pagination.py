from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ChapterPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):

        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'result': data
        })


class ComicPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):

        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'result': data
        })
