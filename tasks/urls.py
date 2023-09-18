from django.urls import path

from tasks.views import (BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView, TaskCreateAPIView,
                         TaskListByColumnAPIView, ColumnListAPIView, BoardDetailRetrieveAPIView)

urlpatterns = [
    path('board_list', BoardListAPIView.as_view(), name='board_list'),
    path('column-list', ColumnListAPIView.as_view(), name='column_list'),
    path('board', BoardCreateAPIView.as_view(), name='board'),
    path('task', TaskCreateAPIView.as_view(), name='task'),
    path('board_id/<int:board_id>', BoardColumnListAPIView.as_view(), name='board_column-list'),
    path('column_id/<int:column_id>', TaskListByColumnAPIView.as_view(), name='column_task_list'),
    path('board_detail/<int:id>', BoardDetailRetrieveAPIView.as_view(), name='board_all'),

]
