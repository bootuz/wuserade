from django.urls import path
from .views import index, get_poem

urlpatterns = [
    path('poems/', index, name='poems_list'),
    path('poems/<int:pk>/', get_poem, name='poem')
]

