from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('account/api/user', views.UserViewSet)
router.register('account/api/category', views.CategoryViewSet)
router.register('account/api/reference', views.ReferenceViewSet)
router.register('account/api/portfolio', views.PortfolioViewSet)

app_name = 'accounts'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('', include(router.urls)),
    path('login-or-signup/', views.LoginOrSignupView.as_view(), name='login-or-signup/'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),

    path('signup/check_username/', views.check_username, name='check_username'),
    path('signup/check_password1/', views.check_password, name='check_password'),
]
