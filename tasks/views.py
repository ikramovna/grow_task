from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from tasks.models import Board, Column
from tasks.pagination import CustomPagination
from tasks.response_json import CustomRenderer
from tasks.serializer import BordModelSerializer, CreateBoardSerializer, ColumnModelSerializer


class BoardListAPIView(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BordModelSerializer


class BoardCreateAPIView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = CreateBoardSerializer
    # renderer_classes = [CustomRenderer]
    # pagination_class = CustomPagination

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

    # Board_id bo'ycha Columns olad
    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        queryset = Column.objects.filter(board_id=board_id)
        return queryset


class ColumnCreateAPIView(CreateAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
