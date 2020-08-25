from django.urls import path, include
# from views import dashboard, logout
from . import views
urlpatterns = [
    # path("", index),
    # path('dashboard', views.dashboard),
    # path('logout', views.logout),
    path('profile/', views.dashboard),
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
]