from django.urls import path

from tasks.views import BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView, TaskCreateAPIView, \
    TaskListByColumnAPIView, ColumnListAPIView

urlpatterns = [
    # path('', include(router.urls)),
    path('board-list', BoardListAPIView.as_view(), name='board-list'),
    path('column-list', ColumnListAPIView.as_view(), name='column-list'),
    path('board-create', BoardCreateAPIView.as_view(), name='board-create'),
    path('task-create', TaskCreateAPIView.as_view(), name='task-create'),
    path('board-column-list/<int:board_id>', BoardColumnListAPIView.as_view(), name='board-column-list'),
    path('column-task-list/<int:column_id>', TaskListByColumnAPIView.as_view(), name='column-task-list'),

]