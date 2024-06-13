from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.index, name = 'index'),
    path("analyzer/", views.analyzer, name = 'analyzer'),
    path("details/", views.details, name = 'details'),
    path("result/", views.MapView.as_view(), name = 'result'),
]
