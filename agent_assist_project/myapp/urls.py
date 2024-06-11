# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('upload/', views.upload_audio, name='upload_audio'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_context_id/', views.get_context_id, name='get_context_id'),
    path('upload/', views.upload_audio, name='upload_audio'),
]

