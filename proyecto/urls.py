from django.urls import path

from proyecto.views import *

urlpatterns = [
    # path('', views.index, name='index'),
    path('', ProyectoView.as_view(), name='proyecto'),
    # path('<int:id>/detalles/', Detalles.as_view(), name='detalles'),
    path('detalle/<int:id>/', Detalles.as_view(), name='detalles'),
    path('uri/', Detalles.detalles, name='uri_info'),
]
