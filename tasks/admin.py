from django.contrib import admin

from tasks.models import Column, Board


class ColumnAdmin(admin.StackedInline):
    model = Column


class BoardAdmin(admin.ModelAdmin):
    inlines = (ColumnAdmin,)


admin.site.register(Board, BoardAdmin)
