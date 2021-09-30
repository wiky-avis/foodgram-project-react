from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions import AdminOrAuthorOrReadOnly
from .models import Subscription
from .serializers import SubscriptionSerializer, CustomUserSerializer

User = get_user_model()


class UserMeViewSet(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomUserViewSet(UserViewSet):
    permission_classes = [AdminOrAuthorOrReadOnly]
    serializer_class = CustomUserSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if (Subscription.objects.filter(user=user, author=author)
                .exists() or user == author):
            return Response({
                'errors': ('Вы уже подписаны на этого пользователя '
                           'или подписываетесь на самого себя')
            }, status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(
            subscribe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = Subscription.objects.filter(
            user=user, author=author
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
