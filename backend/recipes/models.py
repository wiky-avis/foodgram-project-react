from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    title = models.CharField('Название', max_length=50)
    hexcolor = models.CharField(
        'Цветовой HEX-код', max_length=7, default="#49B64E"
    )
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return f'Тег - {self.title}'


class Ingredient(models.Model):
    title = models.CharField('Название', max_length=70)
    quantity = models.PositiveIntegerField('Количество')
    units_measurement = models.CharField('Единицы измерения', max_length=10)

    def __str__(self):
        return f'{self.title} - {self.quantity} - {self.units_measurement}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации (пользователь)'
    )
    title = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка', upload_to='recipe/')
    description = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag, related_name='recipe_tag', blank=True, verbose_name='Тег'
    )
    cooking_time_min = models.PositiveIntegerField(
        'Время приготовления в минутах', validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'Рецепт - {self.title}'
