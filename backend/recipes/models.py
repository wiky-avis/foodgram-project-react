from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=50, db_index=True)
    color = models.CharField(
        'Цветовой HEX-код', max_length=7, default="#49B64E"
    )
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return f'Тег - {self.name}'


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=70, db_index=True)
    quantity = models.PositiveIntegerField('Количество')
    measurement_unit = models.CharField('Единицы измерения', max_length=10)

    def __str__(self):
        return f'{self.name} - {self.quantity} - {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации (пользователь)'
    )
    name = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка', upload_to='recipe/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe_ingredients'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipe_tags', blank=True, verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах', validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'Рецепт - {self.name}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users_favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipes')


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.author}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.recipe}'
