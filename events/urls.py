from django.urls import path
from events.views import \
    CreateEventView, \
    SubmitApplicationView, \
    EventDetailView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='create_event'),
    path(
        '<int:event_id>/apply/',
        SubmitApplicationView.as_view(),
        name='apply',
    ),
    path('<int:event_id>/', EventDetailView.as_view(), name='event_details'),
]
