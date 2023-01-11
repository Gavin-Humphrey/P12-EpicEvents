from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    event_name = filters.CharFilter(method="filter_event_name")
    client_name = filters.CharFilter(
        field_name="contract__client__last_name", lookup_expr="icontains"
    )
    client_email = filters.CharFilter(
        field_name="contract__client__email", lookup_expr="icontains"
    )
    event_after = filters.DateTimeFilter(field_name="event_date", lookup_expr="gte")
    event_before = filters.DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = [
            "event_name",
            "contract__client__last_name",
            "contract__client__email",
            "event_date",
        ]
