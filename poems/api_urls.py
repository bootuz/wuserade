from django.urls import path
from . import api_views

urlpatterns = [
    path('poems/', api_views.poem_list, name='api_poems_list'),
    path('poems/<int:pk>/', api_views.poem_detail, name='api_poem_detail'),
    path('poems/latest/', api_views.latest_poems, name='api_latest_poems'),
    path('poems/search/', api_views.search_poems, name='api_search_poems'),
    path('authors/', api_views.author_list, name='api_authors_list'),
    path('authors/<int:pk>/', api_views.author_detail, name='api_author_detail'),
    path('authors/<int:pk>/poems/', api_views.author_poems, name='api_author_poems'),
    path('themes/', api_views.theme_list, name='api_themes_list'),
    path('themes/<int:pk>/poems/', api_views.theme_poems, name='api_theme_poems'),
    path('poems/featured/', api_views.featured_poem, name='api_featured_poem'),
] 
