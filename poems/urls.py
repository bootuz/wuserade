from django.urls import path
from .views import index, get_poem, get_latest_poems

urlpatterns = [
    path('poems/', index, name='poems_list'),
    path('poems/<int:pk>/', get_poem, name='poem'),
    path('poems/latest/', get_latest_poems, name='latest_poems')
]

