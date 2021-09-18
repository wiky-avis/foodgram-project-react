from django.db import models


class Tag(models.Model):
    title = models.CharField('Название', max_length=70)
    hexcolor = models.CharField('Цветовой HEX-код', max_length=7, default="#49B64E")
    slug = models.SlugField('Slug')


class Ingredient(models.Model):
    title = models.CharField('Название', max_length=70)
    quantity = models.PositiveIntegerField('Количество')
    units_measurement = models.CharField('Единицы измерения', max_length=10)


class Recipe(models.Model):
    author = models.CharField('Автор публикации (пользователь)', max_length=70)
    title = models.CharField('Название', max_length=70)
    image = models.ImageField('Картинка')
    description = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyFiel(Ingredient, verbose_name='Ингредиенты')
    tag = models.ManyToManyField(Tag, verbose_name="Тег")
    cooking_time_min = models.PositiveIntegerField(
        'Время приготовления в минутах'
    )

