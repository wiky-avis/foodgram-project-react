from recipes.models import Subscription
from api.serializers import SubscribeSerializer
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import CurrentUserOrAdmin, GetPost
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [GetPost]

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'],
            permission_classes=[CurrentUserOrAdmin])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        self.request.user.set_password(new_password)
        self.request.user.save()
        return Response(data={}, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscriber__user=request.user).order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        subscribed = user.subscription_on.filter(author=author).exists()
        if request.method == 'GET':
            if author != user and not subscribed:
                Subscription.objects.create(user=user, author=author)
                serializer = UserSerializer(
                    author,
                    context={'request': request}
                )
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {
                'errors': ('Вы или уже подписаны на этого автора, '
                           'или пытаетесь подписаться на себя, что невозможно')
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        if not user.subscription_on.filter(author=author).exists():
            data = {
                'errors': ('Вы не подписаны на данного автора '
                           '(напоминание: на себя подписаться невозможно)')
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
