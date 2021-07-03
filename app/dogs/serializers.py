from rest_framework import serializers
from core.models import Tag, OpsDone


class TagSerializer(serializers.ModelSerializer):
    """serializes the tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class OpsDoneSerializer(serializers.ModelSerializer):
    """serializes the opsdone objects"""

    class Meta:
        model = OpsDone
        fields = ('id', 'name')
        read_only_fields = ('id',)
