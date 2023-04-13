from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from Comics.models import Category, Comic
from Comics.serializers import ComicsSerializer, CategorySerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getCategorys(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''
    categorys = Category.objects.filter(
        Q(name__contains=query)
    )

    serializer = CategorySerializer(categorys, many=True)

    context = {'result': serializer.data, 'count':  categorys.count()}
    return Response(context)


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getCategory(request, pk):
    category = Category.objects.get(_id=pk)
    comics = Comic.objects.filter(category__name__icontains=category)
    serializer = CategorySerializer(category, many=False)
    serializer1 = ComicsSerializer(comics, many=True)
    return Response({'comics': serializer1.data, 'result': serializer.data})
