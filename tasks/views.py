from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from tasks.models import Board, Column, Tasks, Subtasks
from tasks.pagination import CustomPagination
from tasks.response_json import CustomRenderer
from tasks.serializer import (BordModelSerializer, CreateBoardSerializer, ColumnModelSerializer, TaskSerializer,
                              SubtaskSerializer, BoardSerializer)


# Board List
class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BordModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination


# Column List
class ColumnListAPIView(ListAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination


# Get Columns with Board_id

class BoardColumnListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = ColumnModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        queryset = Column.objects.filter(board_id=board_id)
        return queryset


# Get Tasks with Column_id

class TaskListByColumnAPIView(ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination

    def get_queryset(self):
        column_id = self.kwargs['column_id']
        return Tasks.objects.filter(status__id=column_id)




class BoardDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = 'id'


# Board and Column Create

class BoardCreateAPIView(CreateAPIView):
    serializer_class = CreateBoardSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data).data
        board = Board.objects.create(name=serializer.get('name'))
        board.save()
        for column in serializer.get('columns'):
            col = Column.objects.create(board=board, name=column)
            col.save()
        serializer = BordModelSerializer(board, read_only=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Task and Subtask Create

class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        column_id = request.data.get('column_id')

        try:
            column = Column.objects.get(id=column_id)
        except Column.DoesNotExist:
            return Response({"error": "Column does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        task_serializer = self.get_serializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)

        task = task_serializer.save(status=column)

        # Create Subtasks
        subtasks_data = request.data.get('subtasks', [])
        for subtask_data in subtasks_data:
            Subtasks.objects.create(task=task, **subtask_data)

        response_data = {
            'column_id': column_id,
            'title': task.title,
            'description': task.description,
            'difficulty': task.difficulty,
            'subtasks': SubtaskSerializer(task.subtasks, many=True).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
