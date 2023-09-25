from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, BooleanField, TextChoices

from users.models import User


class Board(Model):
    name = CharField(max_length=200)

    def get_columns(self):
        data = []
        for i in self.columns.all():
            data.append(
                {
                    "id": i.id,
                    "name": i.name
                }
            )
        return data

    def __str__(self):
        return self.name


class Column(Model):
    name = CharField(max_length=200)
    board = ForeignKey('Board', CASCADE, related_name='columns')


class Tasks(Model):
    class TypeChoices(TextChoices):
        HART = 'hart', 'Hart'
        MEDIUM = 'medium', ' Medium'
        EASY = 'easy', 'Easy'

    title = CharField(max_length=200)
    description = TextField(blank=True, null=True)
    difficulty = CharField(max_length=220, choices=TypeChoices.choices, default=TypeChoices.EASY)

    column = ForeignKey('Column', CASCADE, related_name='tasks')

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title


class Subtasks(Model):
    name = CharField(max_length=200)
    is_completed = BooleanField(default=False)
    task = ForeignKey('Tasks', CASCADE, related_name='subtasks')


class AuthorTask(Model):
    author = ForeignKey(User, CASCADE)
    task = ForeignKey(Tasks, CASCADE)
