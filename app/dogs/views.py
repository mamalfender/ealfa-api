from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Tag, OpsDone
from dogs import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_permissions(self):
        if self.action == 'create':
            composed_perm = IsAdminUser
            return [composed_perm()]

        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class OpsDoneViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage opsdone in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OpsDone.objects.all()
    serializer_class = serializers.OpsDoneSerializer

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_permissions(self):
        if self.action == 'create':
            composed_perm = IsAdminUser
            return [composed_perm()]

        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new opsdone"""
        serializer.save(user=self.request.user)
