from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Event


class EventFilter(filters.FilterSet):
    event_name = filters.CharFilter(method='filter_event_name')
    client_name = filters.CharFilter(method='filter_client_name')
    client_email = filters.CharFilter(field_name='client__email', lookup_expr='icontains')
    event_after = filters.DateTimeFilter(field_name='event_date', lookup_expr='gte')
    event_before = filters.DateTimeFilter(field_name='event_date', lookup_expr='lte')
  

    class Meta:
        model = Event
        fields = ['event_name', 'client_name', 'contract', 'support_contact', 'event_date', 'location', 'event_status']

   
    def filter_client_name(self, queryset, name, value):
        queryset = queryset.filter(Q(client__first_name__icontains=value) | Q(client__last_name__icontains=value))
        return 