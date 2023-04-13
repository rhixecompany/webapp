from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Comics.models import Comic, Chapter, Page
from Comics.serializers import ComicSerializer, ChapterSerializer, PageSerializer, ComicsSerializer
from django.db.models import Q
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getComics(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''
    comics = Comic.objects.filter(
        Q(title__icontains=query) |
        Q(alternativetitle__contains=query) |
        Q(author__contains=query) |
        Q(artist__contains=query)
    )
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)

    serializer = ComicsSerializer(comics, many=True)

    context = {'result': serializer.data,
               'page': page, 'pages': paginator.num_pages, 'count':  paginator.count}
    return Response(context)


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getTopComics(request):
    comics = Comic.objects.filter(rating__gte=10.0).order_by('rating')
    serializer = ComicsSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([
    AllowAny
])
def getComic(request, pk):
    comic = Comic.objects.get(_id=pk)

    serializer = ComicSerializer(comic, many=False)

    return Response({'comic': serializer.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createComic(request):
    serializer = ComicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateComic(request, pk):
    data = request.data
    user = request.user
    comic = Comic.objects.get(_id=pk)
    comic.user = user
    comic.title = data['title']

    comic.save()
    # comic.genres.add(data['genres'])

    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComic(request, pk):
    comic = Comic.objects.get(_id=pk)
    comic.delete()
    return Response('comic Deleted')


@api_view(['POST'])
@permission_classes([AllowAny])
def uploadImage(request):
    data = request.data
    comicId = data['comic_Id']
    comic = Comic.objects.get(_id=comicId)
    comic.image = request.FILES.get('image')
    comic.save()
    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([
    AllowAny
])
def crawl(request):

    def request(x, s, headers):
        url = f'https://www.asurascans.com/manga/?page={x}'
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, features='lxml')
        content = soup.find_all('div', class_='bsx')
        return content

    def parse(articles, s, headers):
        for item in articles:
            for link in item.find_all('a', href=True):
                links = link['href']
                r = s.get(links, headers=headers)
                soup = BeautifulSoup(r.content, features='lxml')
                title = soup.find("h1", class_="entry-title").text.strip()
                rating = float(soup.find("div", class_="num").text.strip())
                category = soup.find(
                    "div", class_='tsinfo').find("a").text.strip()
                image = soup.find("div", class_="thumb").find('img')['src']
                description = soup.find(
                    "div", class_='entry-content entry-content-single').find("p").text.strip()
                status = soup.find('div', class_='imptdt').find(
                    'i').text.strip()
                author = soup.find('span', class_='author').find(
                    'i').text.strip()
                released = soup.select('div.fmed')[0].find(
                    'span').text.strip()
                artist = soup.select('div.fmed')[1].find(
                    'span').text.strip()
                serialized = soup.select('div.fmed')[2].find(
                    'span').text.strip()

                try:
                    created = soup.select('div.fmed')[4].find(
                        'time').text.strip()
                except:
                    created = ''
                updated = soup.select('div.fmed')[5].find(
                    'time').text.strip()
                # obj, created = Comic.objects.filter(
                #     Q(title__icontains=title)
                # ).get_or_create(image_url=image, rating=rating, status=status, description=description,  author=author,  artist=artist, category=category, serialized=serialized, released=released, created=created, updated=updated, defaults={'title': title})
                comic = {'images': image, 'rating': rating, 'status': status, 'description': description,  'author': author,  'artist': artist,
                         'category': category, 'serialized': serialized, 'released': released, 'created': created, 'updated': updated, 'title': title}
                print(comic)
                chapterslist = soup.select(
                    '.eph-num')[0].find('a')['href']

                r = s.get(chapterslist, headers=headers)
                soup = BeautifulSoup(r.content, features='lxml')
                name = soup.find(
                    "h1", class_="entry-title").text.strip()
                # obj2, created = obj.chapter_set.filter(
                #     Q(name=name)
                # ).get_or_create(comics=obj, name=name, defaults={'name': name})

                posts = soup.select(
                    "div.rdminimal img")
                pages = []
                for p in posts:

                    pages.append(p['src'])
                chapter = {'name': name, 'pages': pages}
                print(chapter)
                # obj3, created = obj2.page_set.filter(
                #     Q(images_url__icontains=pages)
                # ).get_or_create(images_url=pages, chapters=obj2, defaults={'images_url': pages, 'chapters': obj2})
                # obj2.pages.add(obj3)
                # obj2.numPages = obj2.page_set.all().count()
                # obj2.save()
                # obj.numChapters = obj.chapter_set.all().count()
                # obj.save()

    x = 1
    while True:
        print(f'Page {x}')
        starting_time = time.time()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"}
        s = HTMLSession()
        articles = request(x, s, headers)
        x = x+1
        webtoons = parse(articles, s, headers)
        print(webtoons)
        break

        # if len(articles) != 0:
        #     webtoons = parse(articles, s, headers)
        #     print(webtoons)
        # else:
        #     break
    total_time = time.time() - starting_time
    comics = Comic.objects.all()
    chapters = Chapter.objects.all()
    pages = Page.objects.all()
    serializer = ComicSerializer(comics, many=True)
    serializer1 = ChapterSerializer(chapters, many=True)
    serializer2 = PageSerializer(pages, many=True)
    context = {'comics': serializer.data, 'chapters': serializer1.data,
               'pages': serializer2.data, 'totaltime': total_time}
    return Response(context)
