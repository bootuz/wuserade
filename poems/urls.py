from django.urls import path
from .views import (
    index,
    get_poem,
    get_latest_poems,
    get_authors,
    get_author,
    get_poems_of_author,
    search_poems
)

urlpatterns = [
    path('poems/', index, name='poems_list'),
    path('poems/<int:pk>/', get_poem, name='poem'),
    path('poems/latest/', get_latest_poems, name='latest_poems'),
    path('authors/', get_authors, name='authors_list'),
    path('authors/<int:pk>/', get_author, name='author'),
    path('authors/<int:pk>/poems', get_poems_of_author, name='get_poems_of_author'),
    path('poems/search/', search_poems, name='search_poems')
]

