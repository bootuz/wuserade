from rest_framework import serializers
from .models import Poem, Author, Theme, FeaturedPoem


class AuthorSerializer(serializers.ModelSerializer):
    poems_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'poems_count', 'views']


class AuthorDetailSerializer(serializers.ModelSerializer):
    poems_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'photo', 'views', 'created_at', 'poems_count']


class ThemeSerializer(serializers.ModelSerializer):
    poems_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Theme
        fields = ['id', 'title', 'poems_count']


class PoemSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    theme = ThemeSerializer(source='category', read_only=True)
    
    class Meta:
        model = Poem
        fields = ['id', 'title', 'author', 'text', 'theme', 'created_at']

    def get_content(self, obj):
        return obj.text


class PoemDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    theme = ThemeSerializer(source='category', read_only=True)
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = Poem
        fields = ['id', 'title', 'author', 'content', 'theme', 'views', 'likes', 'created_at']
    
    def get_content(self, obj):
        return obj.text 


class FeaturedPoemSerializer(serializers.ModelSerializer):
    poem = PoemDetailSerializer(read_only=True)
    
    class Meta:
        model = FeaturedPoem
        fields = ['featured_date', 'poem']
