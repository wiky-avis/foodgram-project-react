from django.db import models


class Tag(models.Model):
    title = models.CharField('Название', max_length=70)
    hexcolor = models.CharField('Цветовой HEX-код', max_length=7, default="#49B64E")
    slug = models.SlugField('Slug')


class Recipe(models.Model):
    author = models.CharField('Автор публикации (пользователь)', max_length=70)
    title = models.CharField('Название', max_length=70)
    image = models.ImageField('Картинка')
    description = models.TextField('Текстовое описание')
    ingredients = models.CharField('Ингредиенты', max_length=70)
    tag = models.ManyToManyField(Tag, verbose_name="Тег")
    cooking_time_min = models.PositiveIntegerField(
        'Время приготовления в минутах'
    )

