from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tasks.models import Column, Board, Tasks, Subtasks


class ColumnModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ('name', 'board')


class CreateBoardSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    columns = serializers.ListField(child=serializers.CharField())


class BordModelSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ('name',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["columns"] = instance.get_columns()
        return rep


class BoardColumnSerializer(ModelSerializer):
    column = SerializerMethodField()

    def get_choices(self, obj):
        column = Column.objects.filter(name=obj)
        return ColumnModelSerializer(column, many=True).data

    class Meta:
        model = Board
        fields = ('id', 'column')


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtasks
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        exclude = ('status',)


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = '__all__'
