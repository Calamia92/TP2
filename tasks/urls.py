from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TaskViewSet
from .auth_views import register, login, logout

# Créer le routeur pour les ViewSets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

app_name = 'tasks'

urlpatterns = [
    # URLs d'authentification
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # URLs pour les API des tâches
    path('api/', include(router.urls)),
]