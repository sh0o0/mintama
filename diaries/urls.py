from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('diary', views.DiaryViewSet)
router.register('section', views.SectionViewSet)

app_name = 'diaries'
urlpatterns = [
    path('api/', include(router.urls)),
]
