from django.urls import (path, include)
from rest_framework.routers import DefaultRouter 
from equipment import views 

router = DefaultRouter()
router.register('list', views.EquipmentViewSet)
router.register('borrowing', views.BorrowingViewSet)
router.register('history', views.HistoryViewSet)
router.register('users', views.UserViewSet)

app_name = 'equipment'

urlpatterns = [
    path('', include(router.urls))
]
