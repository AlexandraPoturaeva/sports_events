from django.views.generic import FormView
from django.core.paginator import Paginator
from django.shortcuts import render
from events.models import Event
from events.forms import FilterEventsForm


class IndexView(FormView):
    template_name = 'index.html'
    form_class = FilterEventsForm

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()

        sport_kind = request.GET.get('sport_kind')
        region_id = request.GET.get('region')
        dates = request.GET.get('dates')

        not_chosen_filters = ['ALL', None]

        if sport_kind not in not_chosen_filters:
            events = events.filter(sport_kind=sport_kind)

        if region_id not in not_chosen_filters:
            events = events.filter(region=region_id)

        if dates not in not_chosen_filters:
            year, month = dates.split('-')
            events = events.filter(
                date_start__year=year,
                date_start__month=month,
            )

        paginator = Paginator(events, per_page=5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        form = self.form_class(
            initial={
                'sport_kind': sport_kind,
                'region': region_id,
                'dates': dates,
            },
        )

        return render(
            request,
            'index.html',
            {"page_obj": page_obj, 'form': form},
        )
