from django.urls import path, include
from .views import register, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    AnimalViewSet, MilkRecordViewSet, SaleViewSet,
    ExpenseViewSet, FeedStockViewSet, FeedUsageViewSet,
    feed_remaining, profit_loss, monthly_report
)

router = DefaultRouter()
router.register('animals', AnimalViewSet, basename='animal')
router.register('milk', MilkRecordViewSet)
router.register('sales', SaleViewSet)
router.register('expenses', ExpenseViewSet)
router.register('feed-stock', FeedStockViewSet)
router.register('feed-usage', FeedUsageViewSet)

urlpatterns = [
    path('register/', register),
    path('login/', MyTokenObtainPairView.as_view()),  # 👈 custom
    path('refresh/', TokenRefreshView.as_view()),
    path('feed-remaining/', feed_remaining),
    path('profit-loss/', profit_loss),
    path('monthly-report/', monthly_report),
    path('', include(router.urls)),
]

