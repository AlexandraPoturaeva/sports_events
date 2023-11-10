from django.urls import path
from events.views import CreateEventView, SubmitApplicationView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='create_event'),
    path(
        '<int:event_id>/apply/',
        SubmitApplicationView.as_view(),
        name='apply',
    ),
]
