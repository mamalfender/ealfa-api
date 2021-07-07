from rest_framework import serializers
from core.models import Tag, WorkGroup, Animal


class TagSerializer(serializers.ModelSerializer):
    """serializes the tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class WorkGroupSerializer(serializers.ModelSerializer):
    """serializes the WorkGroup objects"""

    class Meta:
        model = WorkGroup
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AnimalSerializer(serializers.ModelSerializer):
    """serializes the Animal objects"""
    work_group = serializers.PrimaryKeyRelatedField(
        label='کارگروه',
        many=True,
        queryset=WorkGroup.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        label='تگ',
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Animal

        fields = ('id', 'species', 'breed', 'name', 'age',
                  'gender', 'support', 'visit_cost', 'med_cost',
                  'op_cost', 'food_cost', 'keep_cost',
                  'sum_cost', 'work_group', 'tags')

        read_only_fields = ('id',)


class AnimalDetailSerializer(AnimalSerializer):
    """serializes animal detail"""
    work_group = WorkGroupSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
