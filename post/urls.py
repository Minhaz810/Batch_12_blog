from django.urls import path
from post.views import post_list_view,post_detail_view,post_create_view

urlpatterns = [
    path('', view=post_list_view,name='post_list'),
    path('<int:pk>/',view=post_detail_view,name='post_detail'),
    path('create_post/',view=post_create_view,name='post_create')
]