from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from Comics.serializers import ChapterSerializer, ChaptersSerializer
from Comics.models import Chapter
from Comics.pagination import ChapterPagination
from rest_framework.response import Response
from rest_framework import filters, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ChapterViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Chapter.objects.all()
    serializer_class = ChaptersSerializer
    pagination_class = ChapterPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class ChapterDetailViewSet(generics.RetrieveAPIView):
    serializer_class = ChapterSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Chapter, slug=item)


class CreateChapter(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        data = request.data
        user = request.user
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapter = serializer.save(user=user)
            chapter.save()

            return Response(serializer.data, status=status.HTTP_200_OK)


class EditChapter(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChapterSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Chapter, name=item)


class DeleteChapter(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChapterSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Chapter, slug=item)
