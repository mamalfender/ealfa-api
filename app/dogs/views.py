from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Tag, OpsDone
from dogs import serializers


class BaseAttrViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin):
    """Manage opsdone in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_permissions(self):
        if self.action == 'create':
            composed_perm = IsAdminUser
            return [composed_perm()]
        elif self.action == 'update':
            composed_perm = IsAdminUser
            return [composed_perm()]
        elif self.action == 'destroy':
            composed_perm = IsAdminUser
            return [composed_perm()]
        elif self.action == 'list':
            composed_perm = IsAuthenticated
            return [composed_perm()]
        elif self.action == 'partial_update':
            composed_perm = IsAdminUser
            return [composed_perm()]
        elif self.action == 'retrieve':
            composed_perm = IsAdminUser
            return [composed_perm()]

        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new opsdone"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class OpsDoneViewSet(BaseAttrViewSet):
    """Manage opsdone in the database"""

    queryset = OpsDone.objects.all()
    serializer_class = serializers.OpsDoneSerializer
