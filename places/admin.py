from django.contrib import admin
from .models import Place, Image

admin.site.register(Place)
admin.site.register(Image)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'lng', 'lat']
    search_fields = ['title']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'position']
    list_editable = ['position']
    list_filter = ['place']