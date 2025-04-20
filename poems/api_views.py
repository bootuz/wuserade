from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q, Count

from .models import Poem, Author, Theme
from .serializers import (
    PoemSerializer,
    PoemDetailSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    ThemeSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page'
    max_page_size = 100


@api_view(['GET'])
def poem_list(request):
    """
    List all poems with pagination
    """
    paginator = StandardResultsSetPagination()
    poems = Poem.objects.all().order_by('-created_at')
    result_page = paginator.paginate_queryset(poems, request)
    serializer = PoemSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def poem_detail(request, pk):
    """
    Retrieve a specific poem by ID
    """
    try:
        poem = Poem.objects.get(id=pk)
        serializer = PoemDetailSerializer(poem)
        return Response(serializer.data)
    except Poem.DoesNotExist:
        return Response(
            {'error': 'Poem does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def search_poems(request):
    """
    Search poems by title or author name
    """
    query = request.query_params.get("q", "")
    if not query:
        return Response(
            {'error': 'Search query parameter "q" is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    poems = Poem.objects.filter(
        Q(title__icontains=query) | Q(author__name__icontains=query)
    ).distinct()
    
    serializer = PoemSerializer(poems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def latest_poems(request):
    """
    Get the 10 latest poems
    """
    latest_poems = Poem.objects.all().order_by('-created_at')[:10]
    serializer = PoemSerializer(latest_poems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def author_list(request):
    """
    List all authors with at least one poem, with pagination
    """
    paginator = StandardResultsSetPagination()
    authors = Author.objects.annotate(
        poems_count=Count('poems')
    ).filter(poems_count__gt=0).order_by('name')
    
    result_page = paginator.paginate_queryset(authors, request)
    serializer = AuthorSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def author_detail(request, pk):
    """
    Retrieve a specific author by ID
    """
    try:
        author = Author.objects.get(id=pk)
        serializer = AuthorDetailSerializer(author)
        return Response(serializer.data)
    except Author.DoesNotExist:
        return Response(
            {'error': 'Author does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def author_poems(request, pk):
    """
    Get all poems by a specific author
    """
    poems = Poem.objects.filter(author_id=pk)
    serializer = PoemSerializer(poems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def theme_list(request):
    """
    List all themes
    """
    themes = Theme.objects.all()
    serializer = ThemeSerializer(themes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def theme_poems(request, pk):
    """
    Get all poems for a specific theme
    """
    poems = Poem.objects.filter(category_id=pk)
    serializer = PoemSerializer(poems, many=True)
    return Response(serializer.data) 
