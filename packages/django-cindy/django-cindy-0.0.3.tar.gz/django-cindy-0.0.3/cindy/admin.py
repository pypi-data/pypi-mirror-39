from django.contrib import admin

from . import models


@admin.register(models.Feed)
class FeedAdmin(admin.ModelAdmin):
    pass
