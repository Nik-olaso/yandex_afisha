from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    """Позволяет добавлять фотографии прямо на странице места"""
    model = Image
    fields = ['image', 'preview', 'position']  # Поля для отображения
    readonly_fields = ['preview']  # Превью только для чтения
    ordering = ['position']
    
    def preview(self, obj):
        """Показывает миниатюру изображения в админке"""
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "Нет изображения"
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    """Админка для модели Place"""
    list_display = ['title', 'images_count']  # Показываем количество фото
    list_filter = ['title']  # Фильтр по названию
    search_fields = ['title']  # Поиск по названию
    fields = ['title', 'description_short', 'description_long', 'lat', 'lng']  # Порядок полей
    inlines = [ImageInline]  # 👈 ГЛАВНОЕ: подключаем Inline для фото
    
    def images_count(self, obj):
        """Показывает количество фотографий у места"""
        return obj.images.count()
    images_count.short_description = "Количество фото"
    images_count.admin_order_field = 'images__count'  # Чтобы можно было сортировать по количеству


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Админка для модели Image (оставлена для отдельного управления)"""
    list_display = ['place', 'image_preview', 'position']  # Показываем превью в списке
    list_filter = ['place']  # Фильтр по местам
    search_fields = ['place__title']  # Поиск по названию места
    fields = ['place', 'image', 'position', 'image_preview']  # Поля для редактирования
    readonly_fields = ['image_preview']  # Превью только для чтения
    raw_id_fields = ['place']  # Удобный поиск места
    
    def image_preview(self, obj):
        """Показывает миниатюру изображения"""
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />')
        return "Нет изображения"
    image_preview.short_description = "Превью"