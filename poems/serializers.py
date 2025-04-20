from rest_framework import serializers
from .models import Poem, Author, Theme


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'photo', 'views', 'created_at']


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title']


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
