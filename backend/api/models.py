from django.db import models


class Recipe(models.Model):
    author = models.CharField('Автор публикации (пользователь)', max_length=70)
    title = models.CharField('Название', max_length=70)
    image = models.ImageField('Картинка')
    description = models.TextField('Текстовое описание')
    ingredients = models.CharField('Ингредиенты', max_length=70)
    tag = models.CharField('Тег', max_length=70)
    cooking_time_min = models.PositiveIntegerField(
        'Время приготовления в минутах'
    )

