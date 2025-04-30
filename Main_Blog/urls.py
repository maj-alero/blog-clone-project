from django.urls import path
from . import views

urlpatterns=[
    path('about/',views.AboutView.as_view(),name='about'),
    path('',views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(),name='new_post'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete_post'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment'),
    path('comment/<int:pk>/approve', views.approve_comment,name='approve_comment'),
    path('comment/<int:pk>/delete', views.delete_comment,name='delete_comment'),
    path('post/<int:pk>/publish/', views.publish_post, name='publish_post'),
    path("search/", views.search_view, name="search"),
    path('account/signup/', views.SignUpView.as_view(), name='signup'),
]