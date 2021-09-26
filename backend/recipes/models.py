from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=50, db_index=True)
    color = models.CharField(verbose_name=(u'Color'), max_length=7, help_text=(u'HEX color, as #RRGGBB'), unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('slug',)

    def __str__(self):
        return f'Тег - {self.name}'


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=70, db_index=True)
    measurement_unit = models.CharField('Единицы измерения', max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации (пользователь)',
        related_name='author_recipes'
    )
    name = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка', upload_to='recipe/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='ingredients_recipes'
    )
    tags = models.ManyToManyField(
        Tag, related_name='tags_recipes', blank=True, verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах', validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт - {self.name}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_subscriber')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipe')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='favorite_recipe_unique')]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscription_on')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='subscriber')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='subscription_unique'
        )]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.author}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='recipe_unique')]

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.recipe}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='amounts')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amounts')
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe_ingredient_unique'
        )]
