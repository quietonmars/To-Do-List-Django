from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from todolist.views import RegisterView, LoginView, LogoutView, TaskViewSet


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # or use obtain_auth_token if you prefer
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('addTask/', TaskCreateView.as_view(), name='addTask'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]