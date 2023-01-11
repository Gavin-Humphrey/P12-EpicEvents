from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Event Info",
            {
                "fields": (
                    "contract",
                    "name",
                    "location",
                    "attendees",
                    "event_date",
                    "event_status",
                )
            },
        ),
        ("Support", {"fields": ("support_contact", "notes")}),
        ("Info", {"fields": ("date_created", "date_updated")}),
    )
    readonly_fields = ("date_created", "date_updated")
    list_display = (
        "id",
        "contract",
        "name",
        "location",
        "support_contact",
        "attendees",
        "event_date",
        "event_status",
        "date_created",
        "date_updated",
    )
    list_filter = ("event_status", "support_contact")
    search_fields = ("client__last_name",)
