from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count

# Create your views here.
from django.http import JsonResponse

from poems.models import Poem, Author, Theme


def index(request):
    poems = Poem.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(poems, 20)

    try:
        poems = paginator.page(page)
    except PageNotAnInteger:
        poems = paginator.page(1)
    except EmptyPage:
        poems = paginator.page(paginator.num_pages)

    poems_data = [
        {
            'id': poem.id,
            'title': poem.title,
            'author': {
                "id": poem.author.id,
                "name": poem.author.name,
            },
            'content': poem.text
        } for poem in poems
    ]

    return JsonResponse(
        {
            'poems': poems_data,
            'total_pages': paginator.num_pages,
            'current_page': page
         },
        safe=False,
    )


def get_poem(request, pk):
    try:
        poem = Poem.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse(
            {'error': 'Poem does not exist'},
            safe=False,
            status=HTTPStatus.NOT_FOUND
        )
    poem_response = {
        'id': poem.id,
        'title': poem.title,
        'author': {
            "id": poem.author.id,
            "name": poem.author.name,
        },
        'content': poem.text
    }
    return JsonResponse(poem_response, safe=False)


def search_poems(request):
    query = request.GET.get("q")
    poems = Poem.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        ).distinct()
    poems_data = [
        {
            'id': poem.id,
            'title': poem.title,
            'author': {
                "id": poem.author.id,
                "name": poem.author.name,
            },
            'content': poem.text
        } for poem in poems
    ]
    return JsonResponse(poems_data, safe=False)


def get_latest_poems(request):
    latest_poems = Poem.objects.all().order_by('created_at')[:10]
    poems_data = [
        {
            'id': poem.id,
            'title': poem.title,
            'author': {
                "id": poem.author.id,
                "name": poem.author.name,
            },
            'content': poem.text
        } for poem in latest_poems
    ]
    return JsonResponse(poems_data, safe=False)


def get_authors(request):
    authors = Author.objects.annotate(poems_count=Count('poems')).filter(poems_count__gt=0).order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(authors, 20)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    author_data = [
        {
            "id": author.id,
            "name": author.name,
        } for author in authors
    ]
    return JsonResponse(
        {
            'authors': author_data,
            'total_pages': paginator.num_pages,
            'current_page': page
         },
        safe=False,
    )


def get_authors_v2(request):
    authors = Author.objects.annotate(poems_count=Count('poems')).filter(poems_count__gt=0).order_by('name')

    author_data = [
        {
            "id": author.id,
            "name": author.name,
        } for author in authors
    ]
    return JsonResponse(author_data, safe=False)


def get_author(request, pk):
    try:
        author = Author.objects.get(id=pk)
        author_data = {
            'id': author.id,
            'name': author.name,
        }
        return JsonResponse(author_data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(
            data={'error': 'Author does not exist'},
            safe=False,
            status=HTTPStatus.NOT_FOUND
        )


def get_poems_of_author(request, pk):
    poems = Poem.objects.filter(author_id=pk)
    poems_data = [
        {
            'id': poem.id,
            'title': poem.title,
            'author': {
                "id": poem.author.id,
                "name": poem.author.name,
            },
            'content': poem.text
        } for poem in poems
    ]
    return JsonResponse(poems_data, safe=False)


def get_themes(request):
    themes = Theme.objects.all()
    theme_data = [
        {
            "id": theme.id,
            "title": theme.title,
        } for theme in themes
    ]
    return JsonResponse(theme_data, safe=False)


def get_poems_by_theme(request, pk):
    poems = Poem.objects.filter(category_id=pk)
    poems_data = [
        {
            'id': poem.id,
            'title': poem.title,
            'author': {
                "id": poem.author.id,
                "name": poem.author.name,
            },
            'content': poem.text
        } for poem in poems
    ]
    return JsonResponse(poems_data, safe=False)
