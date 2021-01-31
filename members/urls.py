from django.contrib import admin, auth
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('admin/register', views.register, name='register'),
    path('admin/users', views.showUsers, name='show_users'),
    path('admin/users/<int:id>', views.userDelete, name='user_delete'),
    path('logout/', authViews.LogoutView.as_view(next_page='/'), name='logout')
]
