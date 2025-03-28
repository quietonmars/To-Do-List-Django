from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from todolist.views import RegisterView, LoginView, LogoutView, UserView
from todolist.viewsets import NoteViewSet

router = routers.DefaultRouter()
# router.register('notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # or use obtain_auth_token if you prefer
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
] + router.urls