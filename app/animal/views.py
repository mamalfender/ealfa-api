from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Animal, Tag, WorkGroup
from animal import serializers


class BaseAttrViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin):
    """Manage workgroup in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_permissions(self):
        if self.action == 'list':
            composed_perm = IsAuthenticated
            return [composed_perm()]
        else:
            composed_perm = IsAdminUser
            return [composed_perm()]

    def perform_create(self, serializer):
        """Create a new workgroup"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class WorkGroupViewSet(BaseAttrViewSet):
    """Manage WorkGroup in the database"""

    queryset = WorkGroup.objects.all()
    serializer_class = serializers.WorkGroupSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    """manage animal objects in the db"""

    serializer_class = serializers.AnimalSerializer
    queryset = Animal.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'list':
            composed_perm = IsAuthenticated
            return [composed_perm()]
        else:
            composed_perm = IsAdminUser
            return [composed_perm()]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.AnimalDetailSerializer

        return self.serializer_class
