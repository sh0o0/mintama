from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView, name='registration')
]
