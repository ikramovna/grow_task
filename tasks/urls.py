from django.urls import path

from tasks.views import (BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView, TaskCreateAPIView,
                         TaskListByColumnAPIView, ColumnListAPIView, BoardDetailRetrieveAPIView,
                         CreateColumnCreateAPIView, BoardUpdateAPIViewDestroyAPIView, ColumnUpdateAPIViewDestroyAPIView,
                         TaskUpdateAPIView, TaskCreateAPIVieww)

urlpatterns = [
    path('board/list', BoardListAPIView.as_view(), name='board'),
    path('board', BoardCreateAPIView.as_view(), name='board'),
    path('board/<int:id>', BoardDetailRetrieveAPIView.as_view(), name='board_detail'),
    path('board/crud/<int:pk>/', BoardUpdateAPIViewDestroyAPIView.as_view(), name='board'),

    path('column/list', ColumnListAPIView.as_view(), name='columns'),
    path('column', CreateColumnCreateAPIView.as_view(), name='column'),
    path('column/<int:board_id>', BoardColumnListAPIView.as_view(), name='columns'),
    path('column/crud/<int:pk>/', ColumnUpdateAPIViewDestroyAPIView.as_view(), name='column'),

    path('task', TaskCreateAPIView.as_view(), name='task'),
    path('task/<int:column_id>', TaskListByColumnAPIView.as_view(), name='tasks'),
    path('task/<int:id>', TaskUpdateAPIView.as_view(), name='tasks-update'),

    path('task_create', TaskCreateAPIVieww.as_view(), name='task_create'),
]
