from django.urls import path
from django.contrib.auth import views
from .views import SignUpView, ProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    #login and logout views are handled in the main urls.py
    path('accounts/login/', views.LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page="/"), name='logout'),
]