from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer, CharField, ListField

from tasks.models import Column, Board, Tasks, Subtasks


class ColumnModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ('id','name', 'board_id')


class CreateBoardSerializer(Serializer):
    name = CharField(max_length=150)
    columns = ListField(child=CharField())


class BordModelSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ('id','name')

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep["columns"] = instance.get_columns()
    #     return rep


class BoardColumnSerializer(ModelSerializer):
    column = SerializerMethodField()

    def get_choices(self, obj):
        column = Column.objects.filter(name=obj)
        return ColumnModelSerializer(column, many=True).data

    class Meta:
        model = Board
        fields = ('id', 'column')


class SubtaskSerializer(ModelSerializer):
    class Meta:
        model = Subtasks
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        exclude = ('status',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "id": representation['id'],
            "title": representation['title'],
            "description": representation['description'],
            "difficulty": representation['difficulty'],
            "subtasks": representation['subtasks']
        }


class ColumnSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = '__all__'


class BoardSerializer(ModelSerializer):
    columns = SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'columns')

    def get_columns(self, obj):
        columns_data = []
        for column in obj.columns.all():
            column_data = {
                'id': column.id,
                'name': column.name,
                'tasks': []
            }
            for task in column.tasks.all():
                task_data = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'difficulty': task.difficulty,
                    'subtasks': []
                }
                for subtask in task.subtasks.all():
                    subtask_data = {
                        'id': subtask.id,
                        'name': subtask.name,
                        'is_completed': subtask.is_completed
                    }
                    task_data['subtasks'].append(subtask_data)
                column_data['tasks'].append(task_data)
            columns_data.append(column_data)
        return columns_data
