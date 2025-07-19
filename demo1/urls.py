from django.urls import path
from . import views

urlpatterns = [
    # ...existing urls...
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]