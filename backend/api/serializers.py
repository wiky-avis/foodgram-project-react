from django.contrib.auth import get_user_model
from recipes.models import (Ingredient, Recipe, RecipeIngredient, Subscription,
                            Tag)
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.serializers import UserSerializer

from .fields import Base64ImageField

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class ShowFollowersSerializer(serializers.ModelSerializer):

    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField('count_author_recipes')
    is_subscribed = serializers.SerializerMethodField('check_if_subscribed')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def count_author_recipes(self, user):
        count_author = user.recipes.all()
        return count_author.count()

    def check_if_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.subscription_on.all()
        if not user.is_authenticated or other_user.count() == 0:
            return False
        return Subscription.objects.filter(user=user,
                                           author=current_user).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeInShoppingList(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.favorite_recipe.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.customers.filter(user=user).exists()


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'recipes', 'recipes_count', 'is_subscribed'
        )
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_recipes(self, obj):
        limit = 10
        try:
            limit = self.context['request'].query_params['recipes_limit']
        except ValueError:
            self.fail('limit is exhausted')
        queryset = obj.author_recipes.all()[:int(limit)]
        serializer = RecipeSerializer(queryset, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()

    def get_recipes_count(self, obj):
        return obj.author_recipes.all().count()


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time')

    def validate_ingredients(self, data):
        ingredients_set = set()
        for item in data:
            amount = item.get('amount')
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    'Количество должно быть > 0'
                )
            identifier = item.get('id')
            if identifier in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients = item.get('ingredients')
            if not ingredients:
                raise serializers.ValidationError(
                    'В рецепте должны быть ингредиенты!'
                )
            ingredients_set.add(identifier)
        return data

    @staticmethod
    def data_collection(recipe, ingredients_data, tags_data):
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            RecipeIngredient.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=recipe, amount=amount
            )
        recipe.tags.clear()
        for tag in tags_data:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        RecipeWriteSerializer.data_collection(
            recipe=recipe,
            ingredients_data=ingredients_data,
            tags_data=tags_data
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        RecipeIngredient.objects.filter(recipe=instance).delete()
        RecipeWriteSerializer.data_collection(
            recipe=instance,
            ingredients_data=ingredients_data,
            tags_data=tags_data
        )
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
