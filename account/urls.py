from django.contrib import admin
from django.urls import path

from .views import LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]
