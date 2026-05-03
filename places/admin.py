from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    fields = ['image', 'preview', 'position']
    readonly_fields = ['preview']
    ordering = ['position']
    
    def preview(self, obj):
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "Нет изображения"
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'images_count']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title', 'description_short', 'description_long', 'lat', 'lng']
    inlines = [ImageInline]
    
    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = "Количество фото"
    images_count.admin_order_field = 'images__count'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'image_preview', 'position']
    list_filter = ['place']
    search_fields = ['place__title']
    fields = ['place', 'image', 'position', 'image_preview']
    readonly_fields = ['image_preview']
    raw_id_fields = ['place']
    
    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />')
        return "Нет изображения"
    image_preview.short_description = "Превью"