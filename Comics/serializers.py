from rest_framework import serializers
from Comics.models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'first_name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_first_name(self, obj):
        first_name = obj.first_name
        if first_name == '':
            first_name = obj.username

        return first_name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email',
                  'first_name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        # fields = ['image_urls','images']
        fields = '__all__'


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = '__all__'


class ComicSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField(read_only=True)
    genres = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comic
        fields = '__all__'

    def get_chapters(self, obj):
        chapters = obj.chapter_set.all()
        serializer = ChapterSerializer(chapters, many=True)
        return serializer.data

    def get_genres(self, obj):
        genres = obj.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return serializer.data

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data


class ComicsSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField(read_only=True)
    genres = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comic
        fields = '__all__'

    def get_chapters(self, obj):
        chapters = obj.chapter_set.all()[0:2]
        serializer = ChapterSerializer(chapters, many=True)
        return serializer.data

    def get_genres(self, obj):
        genres = obj.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return serializer.data

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data


# class ComicCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Comic
#         fields = '__all__'


# class ChaptersSerializer(serializers.ModelSerializer):
#     comic = serializers.SerializerMethodField(read_only=True)
#     comments = serializers.SerializerMethodField(read_only=True)
#     pages = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Chapter
#         fields = '__all__'

#     def get_comic(self, obj):
#         comic = obj.comic
#         serializer = ComicCreateSerializer(comic, many=False)
#         return serializer.data

#     def get_comments(self, obj):
#         comments = obj.comments.all()
#         serializer = CommentSerializer(comments, many=True)
#         return serializer.data

#     def get_pages(self, obj):
#         pages = obj.pages.all()
#         serializer = PageSerializer(pages, many=True)
#         return serializer.data


# class ComicSerializer(serializers.ModelSerializer):
#     chapters = serializers.SerializerMethodField(read_only=True)
#     genres = serializers.SerializerMethodField(read_only=True)
#     category = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Comic
#         fields = '__all__'

#     def get_chapters(self, obj):
#         chapters = obj.chapter_set.all().order_by('-name')[0:2]
#         serializer = ChaptersSerializer(chapters, many=True)
#         return serializer.data

#     def get_genres(self, obj):
#         genres = obj.genres.all()
#         serializer = GenreSerializer(genres, many=True)
#         return serializer.data

#     def get_category(self, obj):
#         category = obj.category
#         serializer = CategorySerializer(category, many=False)
#         return serializer.data


# class ChapterSerializer(serializers.ModelSerializer):
#     pages = serializers.SerializerMethodField(read_only=True)
#     comic = serializers.SerializerMethodField(read_only=True)
#     comments = serializers.SerializerMethodField(read_only=True)
#     chapters = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Chapter
#         fields = '__all__'

#     def get_pages(self, obj):
#         pages = obj.pages.all()
#         serializer = PageSerializer(pages, many=True)
#         return serializer.data

#     def get_comic(self, obj):
#         comic = obj.comic
#         serializer = ComicCreateSerializer(comic, many=False)
#         return serializer.data

#     def get_comments(self, obj):
#         comments = obj.comments.all()
#         serializer = CommentSerializer(comments, many=True)
#         return serializer.data

#     def get_chapters(self, obj):
#         chapters = obj.comic.chapter_set.all()
#         serializer = ChaptersSerializer(chapters, many=True)
#         return serializer.data
