from django.urls import path,include
from .views import register
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet,MilkRecordViewSet,SaleViewSet,ExpenseViewSet,FeedStockViewSet,FeedUsageViewSet,feed_remaining,profit_loss

router = DefaultRouter()
router.register('animals', AnimalViewSet)
router.register('milk', MilkRecordViewSet)
router.register('sales', SaleViewSet)
router.register('expenses', ExpenseViewSet)
router.register('feed-stock', FeedStockViewSet)
router.register('feed-usage', FeedUsageViewSet)


urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('feed-remaining/', feed_remaining),
    path('profit-loss/', profit_loss),
    path('monthly-report/', monthly_report),
    path('', include(router.urls)),
]
