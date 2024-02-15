from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
from django.http import JsonResponse

from poems.models import Poem


def index(request):
    poems = Poem.objects.all().order_by('?')
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
