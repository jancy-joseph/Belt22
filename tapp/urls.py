from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('thoughts',views.wallFrontPageFunc),
    path('logout',views.clearSessionsFunc),
    path('addpost',views.addPostFunc),
    path('<int:my_post_id>/like',views.PostLikeFunc),
    path('<int:my_post_id>/unlike',views.PostUnLikeFunc),
    path('<int:my_post_id>/deletepost',views.DeletePostFunc),
    path('thoughts/<int:my_post_id>',views.ViewUserPostsFunc),
    # path('myaccount/<int:my_user_id>',views.EditMyAccountFunc),
    # path('<int:my_user_id>/Update',views.UpdateMyAccountFunc)
]