""" from django.urls import path
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
 """
from knox import views as knox_views
from .views import *
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("history", AccountViewSet)

urlpatterns = [
    path('api/', include(router.urls), name='history'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change_profile/<int:pk>/', UpdateProfileView.as_view(), name='change-password'),
]