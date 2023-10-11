from django.contrib import admin

# Register your models here.
#from wagtail.contrib.modeladmin.options import (
#    ModelAdmin,
#    modeladmin_register,
#)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Subscribers


class SubscriberAdmin(SnippetViewSet):
    """Subscriber admin."""

    model = Subscribers
    menu_label = "Subscribers"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "full_name",)
    search_fields = ("email", "full_name",)

register_snippet(SubscriberAdmin)
    