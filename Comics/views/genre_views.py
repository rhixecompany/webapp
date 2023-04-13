from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Comics.models import Genre, Comic
from Comics.serializers import ComicsSerializer, GenreSerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getGenres(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''
    genres = Genre.objects.filter(
        Q(name__contains=query)
    )
    page = request.GET.get('page')
    paginator = Paginator(genres, 20)
    try:
        genres = paginator.page(page)
    except PageNotAnInteger:
        genres = paginator.page(1)
    except EmptyPage:
        genres = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)

    serializer = GenreSerializer(genres, many=True)

    context = {'result': serializer.data,
               'page': page, 'pages': paginator.num_pages, 'count':  paginator.count}
    return Response(context)


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getGenre(request, pk):
    genre = Genre.objects.get(_id=pk)
    comics = Comic.objects.filter(genres__name__icontains=genre)
    serializer = GenreSerializer(genre, many=False)
    serializer1 = ComicsSerializer(comics, many=True)
    return Response({'comics': serializer1.data, 'result': serializer.data})
