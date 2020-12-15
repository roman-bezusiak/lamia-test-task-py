from django.urls import path

from .views import MovieJSONView

urlpatterns = [
    path('', MovieJSONView.as_view()),
]