from django.urls import path
from . import views


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.create_post, name="create_post"),
    path("<int:post_id>/edit/",views.update_post,name="update_post"),
    path("<int:post_id>/delete/",views.delete_post,name="delete_post"),
    path("api/posts/",views.api_post_list,name="api_post_list"),
    path("api/posts/<int:post_id>/",views.api_post_detail,name="api_post_detail"),
]