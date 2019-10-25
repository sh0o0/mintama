from django.urls import path, include
from rest_framework import routers

from .accounts.viewsets import OwnUserViewSet, UserViewSet, CategoryViewSet, ReferenceViewSet, PortfolioViewSet
from .notes.viewsets import NoteViewSet, SectionViewSet, ReviewViewSet
from .todos.viewsets import BoardViewSet, ListViewSet, CardViewSet


general_router = routers.DefaultRouter()
detail_router = routers.DefaultRouter()


general_router.register('own', OwnUserViewSet)
general_router.register('categories', CategoryViewSet)
general_router.register('users', UserViewSet)
general_router.register('reviews', ReviewViewSet)

detail_router.register('references', ReferenceViewSet)
detail_router.register('portfolios', PortfolioViewSet)
detail_router.register('notes', NoteViewSet)
detail_router.register('sections', SectionViewSet)
detail_router.register('boards', BoardViewSet)
detail_router.register('lists', ListViewSet)
detail_router.register('cards', CardViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(general_router.urls)),
    path('', include(detail_router.urls)),
    path('accounts/<slug:username>/', include(detail_router.urls))
]