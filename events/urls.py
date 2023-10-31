from django.urls import path
from events.views import CreateEventView

urlpatterns = [
    path('create/', CreateEventView.as_view()),
]
