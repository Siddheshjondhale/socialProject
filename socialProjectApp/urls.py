from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_fake_account, name='predict_fake_account'),
]
