from django.urls import path

from tasks.views import (BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView, TaskCreateAPIView,
                         TaskListByColumnAPIView, ColumnListAPIView, BoardDetailRetrieveAPIView)

urlpatterns = [
    path('board/list', BoardListAPIView.as_view(), name='board'),
    path('column/list', ColumnListAPIView.as_view(), name='columns'),
    path('board', BoardCreateAPIView.as_view(), name='board'),
    path('task', TaskCreateAPIView.as_view(), name='task'),
    path('column/<int:board_id>', BoardColumnListAPIView.as_view(), name='columns'),
    path('task/<int:column_id>', TaskListByColumnAPIView.as_view(), name='tasks'),
    path('board/<int:id>', BoardDetailRetrieveAPIView.as_view(), name='board_detail'),

]
