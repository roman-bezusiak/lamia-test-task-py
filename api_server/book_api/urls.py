from django.urls import path

from .views import BookJSONView

urlpatterns = [
    path('', BookJSONView.as_view()),
]