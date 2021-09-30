from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField('Тег', max_length=200, unique=True,)
    color = models.CharField(max_length=7, default='#ffffff', unique=True)
    slug = models.SlugField("Slug", unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор',
        null=True,)
    name = models.CharField(
        max_length=200,
        verbose_name='Название',)
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение',
        null=True, blank=True
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
        verbose_name='Ингредиент',)
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тег')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупка',)
    added_dt = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,)

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_list')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients_in_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes_ingredients_list'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[MinValueValidator(
            1,
            "Количество ингредиентов должно быть больше 0"), ]
    )

    class Meta:
        verbose_name = 'Количество игредиентов в рецепте'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipes')
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    added_dt = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorites_recipes')
        ]

    def __str__(self):
        return (f'Пользователь: {self.user}, '
                f'избранные рецепты: {self.recipe.name}')
