from django.contrib import admin

from models import Crime


class CrimeAdmin(admin.ModelAdmin):
    list_filter = ('date', 'updated_at')
    ordering = ('headline',)
    search_fields = ('headline',)
admin.site.register(Crime, CrimeAdmin)
