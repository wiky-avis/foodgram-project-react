from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
# v1_router.register('users', UserViewSet)
# v1_router.register(
#     r'users/(?P<title_id>\d+)', UserProfileViewSet,)
# v1_router.register(
#     r'users/(?P<title_id>\d+)/subscribe', SubscribeViewSet)
# v1_router.register('tags', TagViewSet)
# v1_router.register('tags/(?P<title_id>\d+)', TagDetailViewSet)
# v1_router.register('recipes', RecipeViewSet)
# v1_router.register('recipes/(?P<title_id>\d+)', ResipeDetailViewSet)
# v1_router.register('recipes/(?P<title_id>\d+)/shopping_cart', ShoppingCartViewSet)
# v1_router.register('recipes/(?P<title_id>\d+)/favorite', FavoriteViewSet)
# v1_router.register('ingredients', UserViewSet)
# v1_router.register(
#     r'ingredients/(?P<title_id>\d+)', UserProfileViewSet)


urlpatterns = [
    path('', include(v1_router.urls)),
    # path('auth/token/login', Joser.as_view(), name='get_token'),
]
