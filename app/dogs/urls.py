from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dogs import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('opsdone', views.OpsDoneViewSet)


app_name = 'dogs'

urlpatterns = [
    path('', include(router.urls))
]
