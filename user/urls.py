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
    path('registration/', views.RegistrationView, name='registration'),
    path('api/', views.UserViewset, name='user_api'),
]
