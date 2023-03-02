from django.urls import path

from .views import PostView, PostListView, delete_comment, CreatePost, delete_post

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostView.as_view(), name='post'),
    path('del_comment/<int:id_comment>/<int:id_author>', delete_comment, name='delete-comment'),
    path('create/', CreatePost.as_view(), name='post-create'),
    path('del_post/<int:id_post>', delete_post, name='delete-post')
]
