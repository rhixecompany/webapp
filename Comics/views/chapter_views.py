from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status, permissions
from Comics.models import Chapter, Comic, Page, Comment
from Comics.serializers import ChapterSerializer, ComicSerializer, PageSerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getChapters(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''

    chapters = Chapter.objects.filter(
        name__contains=query)

    page = request.GET.get('page')
    paginator = Paginator(chapters, 800)
    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)

    serializer = ChapterSerializer(chapters, many=True)

    context = {'result': serializer.data, 'count':  paginator.count,
               'page': page, 'pages': paginator.num_pages}
    return Response(context)


@api_view(['GET'])
@permission_classes([AllowAny])
def getChapter(request, pk):
    chapter = Chapter.objects.get(_id=pk)
    pages = chapter.pages.all()
    comicId = chapter.comic
    comic = Comic.objects.get(title=comicId)

    serializer = ChapterSerializer(chapter, many=False)
    serializer1 = ComicSerializer(comic, many=False)

    serializer3 = PageSerializer(pages, many=True)
    return Response({'chapter': serializer.data, 'pages': serializer3.data, 'comic': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createChapter(request):

    chapter = Chapter.objects.create(
        name="Sample Name",

    )
    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateChapter(request, pk):
    data = request.data
    user = request.user
    chapter = Chapter.objects.get(_id=pk)
    comic = chapter.comic

    chapter.name = data['name']
    chapter.user = user
    chapter.comic = comic
    chapter.numReviews = chapter.numReviews
    chapter.numPages = chapter.numPages
    chapter.pages = chapter.pages
    chapter.save()

    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteChapter(request, pk):
    chapter = Chapter.objects.get(_id=pk)
    chapter.delete()
    return Response('Chapter Deleted')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createChapterReview(request, pk):
    user = request.user
    chapter = Chapter.objects.get(_id=pk)
    comic = Comic.objects.get(id=chapter.comic._id)
    data = request.data

    # 1 - Review already exists
    alreadyExists = chapter.comments.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Chapter already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Comment.objects.create(
            user=user,
            chapter=chapter,
            comic=comic,
            rating=data['rating'],
            text=data['text'],
        )
        chapter.user = user
        chapter.comic.user = user
        reviews = chapter.comments.all()
        chapter.numReviews = len(reviews)
        chapter.comic.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        chapter.rating = total / chapter.numReviews
        chapter.save()
        chapter.comic.save()
        return Response('Review Added')
