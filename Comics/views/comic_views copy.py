from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from Comics.serializers import ComicSerializer, ChapterSerializer, ComicCreateSerializer
from Comics.models import Comic, Chapter, Page, Genre, Category, Website
from Comics.pagination import ComicPagination
from rest_framework.response import Response
from rest_framework import filters, generics, status
from django.shortcuts import render
import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup
from Comics.forms import ComicDownloadsForm
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes


class ComicViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    pagination_class = ComicPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


class ComicTopViewSet(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Comic.objects.filter(rating__gte=10).order_by('-rating')
    serializer_class = ComicSerializer


@api_view(['GET'])
def getComic(request, pk):
    comic = Comic.objects.get(slug=pk)
    chapters = comic.chapter_set.all()
    serializer = ComicSerializer(comic, many=False)
    serializer1 = ChapterSerializer(chapters, many=True)
    context = {'result': serializer.data, 'chapters': serializer1.data}
    return Response(context)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createComic(request):
    user = request.user
    comic = Comic.objects.create(
        user=user,
        title='Sample Title',
        slug='sample-slug',
        rating=0,
        status='Coming Soon',
        numChapters=0,
        alternativetitle='Sample Alternativetitle',
        description='',
        image_urls="https://www.asurascans.com/wp-content/uploads/2021/09/Untitled-1-ii.jpg",
    )
    serializer = ComicCreateSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateComic(request, pk):
    data = request.data

    comic = Comic.objects.get(slug=pk)
    comic.user = request.user
    comic.title = data['title']
    comic.rating = data['rating']
    comic.status = data['status']
    comic.numChapters = data['numChapters']
    comic.alternativetitle = data['alternativetitle']
    comic.description = data['description']
    comic.save()

    serializer = ComicCreateSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComic(request, pk):
    comic = Comic.objects.get(title=pk)
    comic.delete()
    return Response('Comic Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    comicid = data['comicid']
    comic = Comic.objects.get(id=comicid)

    comic.image = request.FILES.get('image')
    comic.save()

    return Response('Image was uploaded')


async def get_pages(session, url):
    async with session.get(url) as res:
        if res.status == 200:
            data = await res.text()
            soup = BeautifulSoup(data, 'html.parser')
            page = [article.find('a')['href'] for article in soup.find_all(
                'div', {"class": "bsx"})]
            print(f'Link:{res.url}')
            return page


async def get_comics(session, url):
    async with session.get(url) as res:

        if res.status == 200:
            data = await res.text()
            soup = BeautifulSoup(data, 'html.parser')
            title = soup.find(
                "h1", class_="entry-title").text.strip()
            link = soup.find(
                "div", class_="thumb").find('img')['src']
            try:
                description = [des.text.strip().replace('\n ', '') for des in soup.find(
                    attrs={"itemprop": "description"}).select('p')]
            except:
                description = ''
            slug = soup.find_all(attrs={"itemprop": "item"})[
                1]['href'].split('/')[-2]
            try:
                alternativetitle = soup.find(
                    'div', {'class': 'wd-full'}).find('span').text.strip()
            except:
                alternativetitle = ''
            try:
                genres = [gen.text.strip() for gen in soup.find(
                    'span', {'class': 'mgen'}).find_all(attrs={"rel": "tag"})]
            except:
                genres = ''
            try:
                numChapters = soup.select('.chapternum')
            except:
                numChapters = ''
            rating = soup.find(
                attrs={"itemprop": "ratingValue"}).text.strip()
            status = soup.find(
                'div', {'class': 'imptdt'}).find('i').text.strip()
            category = soup.find_all(
                'div', {'class': 'imptdt'})[1].find('a').text.strip()
            released = soup.select('.fmed')[0].find(
                'span').text.strip()

            author = soup.select('.fmed')[1].find(
                'span').text.strip()

            artist = soup.select('.fmed')[2].find(
                'span').text.strip()
            serialization = soup.select(
                '.fmed')[3].find('span').text.strip()
            try:
                created_by = soup.select('.fmed')[4].find(attrs={"itemprop": "author"}).find(
                    attrs={"itemprop": "name"}).text.strip()
            except:
                created_by = ''
            try:
                urls = soup.select(
                    '.eph-num')[0].find('a')['href']
                # urls = [url['href']for url in soup.select_one('#chapterlist').select('a')]
            except:
                urls = ''
            comic = {'title': title, 'alternativetitle': alternativetitle, 'slug': slug, 'link': link,
                     'description': description, 'genres': genres, 'numChapters': len(numChapters), 'rating': rating, 'status': status, 'category': category, 'released': released,  'author': author,  'artist': artist, 'serialization': serialization, 'created_by': created_by, 'urls': urls}
            print(f'Comic-Link:{res.url}')
            return comic


async def get_chapters(session, url):
    async with session.get(url) as res:
        if res.status == 200:
            data = await res.text()
            soup = BeautifulSoup(
                data, 'html.parser')
            name = soup.find(
                "h1", class_="entry-title").text.strip()
            pages = [img['src'] for img in soup.select_one(
                '#readerarea').find_all('img', src=True)]
            slug = soup.find('div', {"class": "allc"}).find('a')[
                'href'].split('/')[-2]
            chapter = {'name': name, 'pages': pages, 'slug': slug}
            print(f'Chapter-Link:{res.url}')
            return chapter


async def scraper(request):
    form = ComicDownloadsForm()
    comics = Comic.objects.all()
    chapters = Chapter.objects.all()
    comic_count = comics.count()
    chapter_count = chapters.count()

    if ('url' in request.GET or 'link' in request.GET):
        print(request.GET)
        starting_time = time.time()
        form = ComicDownloadsForm(request.GET)
        if form.is_valid():
            website, created = Website.objects.get_or_create(
                url=form.cleaned_data['url'])
            try:
                newurl = website
            except:
                newurl = form.cleaned_data['url']
            page_actions = []
            comic_actions = []
            chapter_actions = []
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                for num in range(1, 2):

                    url = f'{newurl}/?page={num}&order=update'
                    page_actions.append(
                        asyncio.ensure_future(get_pages(session, url)))
                page_res = await asyncio.gather(*page_actions)
                for pages in page_res:
                    for page in pages:
                        comic_actions.append(asyncio.ensure_future(
                            get_comics(session, page)))
                comic_res = await asyncio.gather(*comic_actions)
                for data1 in comic_res:
                    obj2, created = Category.objects.filter(
                        Q(name__icontains=data1['category'])
                    ).get_or_create(
                        name=data1['category'])
                    try:
                        numCha = data1['numChapters']
                        numChapters = len(numCha)
                    except:
                        pass
                    try:
                        obj, created = Comic.objects.filter(
                            Q(title__icontains=data1['title'])
                        ).get_or_create(user=request.user, source=website, title=data1['title'], slug=data1['slug'], image_urls=data1['link'],  rating=data1['rating'], status=data1['status'], description=data1['description'], released=data1['released'],  author=data1['author'],  artist=data1['artist'], alternativetitle=data1['alternativetitle'], serialization=data1['serialization'], created_by=data1['created_by'], category=obj2, numChapters=numChapters)
                    except:

                        print(data1['title'] + 'Found in database')
                        for genre in data1['genres']:
                            obj1, created = Genre.objects.filter(
                                Q(name__icontains=genre)
                            ).get_or_create(
                                name=genre)
                            try:
                                obj.genres.add(obj1)
                                obj.save()
                            except:
                                pass

                        chapterurls = data1['urls']
                        if chapterurls != '':
                            chapter_actions.append(asyncio.ensure_future(
                                get_chapters(session, chapterurls)))
                        else:
                            print(data1['title'] + 'has no Chapters')
                chapter_res = await asyncio.gather(*chapter_actions)
                for data2 in chapter_res:
                    comic = Comic.objects.get(slug=data2['slug'])
                    if comic:
                        pages = data2['pages']
                        try:
                            obj3, created = Chapter.objects.filter(
                                Q(name__icontains=data2['name'])
                            ).get_or_create(user=request.user, comic=comic, name=data2['name'], numPages=len(pages))
                            for img in pages:
                                obj4, created = Page.objects.filter(
                                    Q(image_urls__icontains=img)
                                ).get_or_create(chapter=obj3, image_urls=img)
                                obj3.pages.add(obj4)
                                obj3.save()
                        except:
                            pass
                            print(data2['name'] + 'Found in database')
            total_time = time.time() - starting_time
            return render(request, 'frontend/scraper.html', {'form': form, 'form': form, 'comics': comics,  'comic_count': comic_count,
                                                             'chapters': chapters,  'chapter_count': chapter_count, 'time': total_time})
    return render(request, 'frontend/scraper.html', {'form': form, 'form': form, 'comics': comics,  'comic_count': comic_count,
                                                     'chapters': chapters,  'chapter_count': chapter_count})
