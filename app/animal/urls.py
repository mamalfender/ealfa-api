from django.urls import path, include
from rest_framework.routers import DefaultRouter

from animal import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('workgroup', views.WorkGroupViewSet)
router.register('animal', views.AnimalViewSet)


app_name = 'animal'

urlpatterns = [
    path('', include(router.urls))
]
