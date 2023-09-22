from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import count_words

urlpatterns = [
    path('', count_words),
]

urlpatterns = format_suffix_patterns(urlpatterns)