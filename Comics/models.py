from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
# Create your models here.


def comics_images_location(instance, filename):
    return '{}/{}'.format(str(instance.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""), filename)


def comics_chapters_images_location(instance, filename):
    return '{}/{}/{}'.format(str(instance.chapter.comic.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""),  instance.chapter.name, filename)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Website(models.Model):
    url = models.URLField(max_length=10000, unique=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.url


class Comic(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(Q(status='Completed') |
                                                 Q(status='Ongoing') |
                                                 Q(status='Dropped'))

    options = (
        ('Completed', 'completed'),
        ('Ongoing', 'ongoing'),
        ('Dropped', 'dropped'),
        ('Coming_Soon', 'coming_soon'),
        ('Hiatus', 'hiatus'),
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.ForeignKey(
        Website, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(
        Genre, related_name='genre', blank=True)
    title = models.CharField(
        max_length=1000, unique=True)
    alternativetitle = models.CharField(max_length=1000, null=True, blank=True)
    slug = models.CharField(max_length=1000, unique=True,)
    description = models.TextField(null=True, blank=True)
    image_urls = models.URLField(max_length=10000)
    images = models.ImageField(_("Images"),
                               max_length=100000, upload_to=comics_images_location)
    rating = models.DecimalField(
        max_digits=9, decimal_places=1, null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=options)
    author = models.CharField(max_length=100, null=True, blank=True)
    artist = models.CharField(max_length=100, null=True, blank=True)
    released = models.CharField(max_length=100, null=True, blank=True)
    serialization = models.CharField(max_length=1000, null=True, blank=True)
    created_by = models.CharField(max_length=1000, null=True, blank=True)
    numChapters = models.IntegerField(default=0)
    numReviews = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    # Users Bookmarks And Likes
    favourites = models.ManyToManyField(
        User, related_name='favourite', blank=True)
    likes = models.ManyToManyField(
        User, related_name='like',  blank=True)
    like_count = models.IntegerField(default=0)
    _id = models.AutoField(primary_key=True, editable=False)
    objects = models.Manager()  # default manager
    newmanager = NewManager()

    class Meta:
        ordering = ['-updated', 'title']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.images.delete()
        super().delete(*args, **kwargs)


class Chapter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.ForeignKey(
        Website, on_delete=models.SET_NULL, null=True, blank=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    name = models.CharField(max_length=10000)
    slug = models.CharField(max_length=10000, unique=True)
    pages = models.ManyToManyField(
        'Page', related_name='page', blank=True)
    numPages = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['-updated', 'name']

    def __str__(self):
        return self.name


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    images = models.ImageField(_("Images"),
                               max_length=100000, upload_to=comics_chapters_images_location)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.chapter.name)

    def delete(self, *args, **kwargs):
        self.images.delete()
        super().delete(*args, **kwargs)


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='owner',
                              on_delete=models.CASCADE, default=None, blank=True)
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='chaptercomments')
    comic = models.ForeignKey(Comic, related_name='comiccomments',
                              on_delete=models.CASCADE, default=None, blank=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.content
