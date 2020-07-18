from django.urls import path,include
from .views import (
    blog_post_create_view,
    blog_post_details_view,
    blog_post_list_view,
    blog_post_update_view,
    blog_post_delete_view,
)

urlpatterns = [

    path('',blog_post_list_view),
    # path('blog/<int:post_id>/',blog_post_detail_page),
    path('<str:slug>',blog_post_details_view),
    path('<str:slug>/edit/',blog_post_update_view),
    path('<str:slug>/delete/',blog_post_delete_view),
    


]
