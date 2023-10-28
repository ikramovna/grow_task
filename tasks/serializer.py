from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer, CharField, ListField

from tasks.models import Column, Board, Tasks, Subtasks, AuthorTask
from users.models import User


class ColumnModelSerializer(ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'name', 'board_id')


class CreateBoardSerializer(Serializer):
    name = CharField(max_length=150)
    columns = ListField(child=CharField())


class BordModelSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name')

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
        fields = ['name']


class TaskSerializer(ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Tasks
        fields = ['column', 'title', 'description', 'difficulty', 'subtasks']

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        column = validated_data.pop('column')
        task = Tasks.objects.create(column=column, **validated_data)

        for subtask_data in subtasks_data:
            Subtasks.objects.create(task=task, **subtask_data)

        return task


class TaskUpdateModelSerializer(ModelSerializer):
    column_id = serializers.IntegerField()

    class Meta:
        model = Tasks
        fields = ("id", "title", "description", "column_id")


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


class TaskCreateModelSerializer(serializers.ModelSerializer):
    subtasks = serializers.ListField(write_only=True, required=False)
    authors = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Tasks
        fields = ('id', 'column', 'title', 'description',  'difficulty', 'subtasks', 'authors')

    def to_representation(self, instance: Tasks):
        rep = super().to_representation(instance)
        rep['author'] = instance.authortask_set.values('author__username', 'author__email')
        return rep

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        authors_data = validated_data.pop('authors', [])

        task = Tasks.objects.create(**validated_data)

        for subtask_name in subtasks_data:
            Subtasks.objects.create(name=subtask_name, task=task)

        author_task = []
        for author_email in authors_data:
            if User.objects.filter(email=author_email).exists():
                user = User.objects.filter(email=author_email).first()
                author_task.append(AuthorTask(task=task, author=user))
        AuthorTask.objects.bulk_create(author_task)

        return task
