from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from tasks.models import Board, Column, Tasks, Subtasks
from tasks.pagination import CustomPagination
from tasks.response_json import CustomRenderer
from tasks.serializer import (BordModelSerializer, CreateBoardSerializer, ColumnModelSerializer, TaskSerializer)


class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BordModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination

class ColumnListAPIView(ListAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination


class BoardCreateAPIView(CreateAPIView):
    serializer_class = CreateBoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data).data
        board = Board.objects.create(name=serializer.get('name'))
        board.save()
        for column in serializer.get('columns'):
            col = Column.objects.create(board=board, name=column)
            col.save()
        serializer = BordModelSerializer(board, read_only=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardColumnListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = ColumnModelSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination

    # Get columns from board ID
    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        queryset = Column.objects.filter(board_id=board_id)
        return queryset


class TaskListByColumnAPIView(ListAPIView):
    serializer_class = TaskSerializer
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination

    # Get tasks from column ID
    def get_queryset(self):
        column_id = self.kwargs['column_id']
        return Tasks.objects.filter(status__id=column_id)


class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer

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

        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
