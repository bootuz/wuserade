from django.core.exceptions import ObjectDoesNotExist
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
    page_size = 21
    page_query_param = 'page'
    page_size_query_param = 'page_size'
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
    except ObjectDoesNotExist:
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
    Get the 9 latest poems
    """
    latest_poems = Poem.objects.all().order_by('-created_at')[:9]
    serializer = PoemSerializer(latest_poems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def author_list(request):
    """
    List all authors with at least one poem, including poem count
    """
    authors = Author.objects.annotate(
        poems_count=Count('poems')
    ).filter(poems_count__gt=0).order_by('name')
    
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def author_detail(request, pk):
    """
    Retrieve a specific author by ID with poem count
    """
    try:
        author = Author.objects.annotate(
            poems_count=Count('poems')
        ).get(id=pk)

        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        # Get or initialize viewed_authors as a set
        viewed_authors = set(request.session.get('viewed_authors', []))

        # Check if an author hasn't been viewed in this session
        if str(pk) not in viewed_authors:
            author.views += 1
            author.save()

            # Add to viewed set and update session
            viewed_authors.add(str(pk))
            request.session['viewed_authors'] = list(viewed_authors)
            request.session.modified = True  # Force session save

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
