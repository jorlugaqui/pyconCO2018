from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ('petal_width', 'petal_length', 'classification', 'created_at')
    list_display = readonly_fields
