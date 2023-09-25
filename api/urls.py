from django.urls import path, include
from .views import ModulViewSet, PostViewSet, AddPermissionForUser
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'moduls', ModulViewSet, basename='modul')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'perms', AddPermissionForUser, basename='perms')


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]