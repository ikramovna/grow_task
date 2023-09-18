from django.urls import path

from tasks.views import BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView, TaskCreateAPIView, \
    TaskListByColumnAPIView, ColumnListAPIView

urlpatterns = [
    # path('', include(router.urls)),
    path('board_list', BoardListAPIView.as_view(), name='board-list'),
    path('column-list', ColumnListAPIView.as_view(), name='column-list'),
    path('board', BoardCreateAPIView.as_view(), name='board-create'),
    path('task', TaskCreateAPIView.as_view(), name='task-create'),
    path('board_id/<int:board_id>', BoardColumnListAPIView.as_view(), name='board-column-list'),
    path('column_id/<int:column_id>', TaskListByColumnAPIView.as_view(), name='column-task-list'),

]