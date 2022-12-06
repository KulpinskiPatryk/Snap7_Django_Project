from django.urls import path
from . import views

app_name = 'Visual_Ploter_Snap'


urlpatterns = [
    path("", views.index, name="index"),
]
