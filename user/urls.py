from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('user', views.UserViewset)

app_name = 'user'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('router', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('entry-user-detail/', views.EntryUserDetailView.as_view(), name='entry_user_detail'),
    path('entry-user-detail/confirm/', views.EntryUserDetailConfirmView.as_view(), name='entry_user_detail_confirm'),
    path('add-user-detail/', views.AddUserDetailView.as_view(), name='add_user_detail'),
    path('api/', views.UserViewset, name='user_api'),

    path('signup/check_username/', views.check_username, name='check_username'),
    path('signup/check_password1/', views.check_password, name='check_password'),
]
