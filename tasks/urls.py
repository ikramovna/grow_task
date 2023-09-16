from django.urls import path

from tasks.views import BoardListAPIView, BoardCreateAPIView, BoardColumnListAPIView

urlpatterns = [
    # path('', include(router.urls)),
    path('board-list', BoardListAPIView.as_view(), name='board-list'),
    path('board-create', BoardCreateAPIView.as_view(), name='board-create'),
    path('board-column-list/<int:board_id>', BoardColumnListAPIView.as_view(), name='board-column-list'),
]