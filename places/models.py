from django.db import models
from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    short_description = models.TextField('Короткое описание')
    long_description = HTMLField('Полное описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title
    

class Image(models.Model):
    place = models.ForeignKey(
        Place, 
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        'Картинка',
        null=True,
        blank=True,
    )
    position = models.PositiveIntegerField(
        'Позиция',
        default=0,
        db_index=True
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['position']

    def __str__(self):
        return f'{self.position} {self.place.title}'