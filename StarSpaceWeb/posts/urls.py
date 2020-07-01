from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create', views.CreatePost.as_view(), name='create'),
    path('by/<slug:username>', views.UserPosts.as_view(), name='for_user'),
    path('by/<slug:username>/<slug:pk>', views.PostDetail.as_view(), name='single'),
    path('create/comment', views.CreateComment.as_view(), name='create_comment')
]
