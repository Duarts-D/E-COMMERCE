from django.urls import path
from apps.permissions.views import Permissoes


app_name = 'permissions'

urlpatterns = [
    path('', Permissoes.as_view(),name='permissions')
]