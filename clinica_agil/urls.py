
from django.contrib import admin
from django.urls import include, path
from consultas import views
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('consultas/', include('consultas.urls')),
]
