from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Полное описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

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
        'Картинки',
        null=True,
        blank=True,
    )
    position = models.PositiveIntegerField(
        'Позиция',
        default=0,
        db_index=True
    )

    def __str__(self):
        return f'{self.position} {self.place.title}'