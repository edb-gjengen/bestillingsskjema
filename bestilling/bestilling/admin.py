from django.contrib import admin
from django.contrib.contenttypes import generic

from bestilling.models import Attachment
from prm.models import PrmOrder
from tekst.models import TekstOrder
from design.models import DesignOrder


class UploadedFileline(generic.GenericTabularInline):
    model = Attachment
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        UploadedFileline,
    ]

admin.site.register(PrmOrder, OrderAdmin)
admin.site.register(TekstOrder, OrderAdmin)
admin.site.register(DesignOrder, OrderAdmin)
admin.site.register(Attachment)