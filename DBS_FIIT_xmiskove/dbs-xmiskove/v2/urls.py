from django.urls import path
from . import views

urlpatterns = [
    path('patches/',views.patch3s),
    path('players/<player_id>/game_exp/',views.funct1on),
    path('players/<player_id>/game_objectives/',views.funct2on),
    path('players/<player_id>/abilities/',views.funct3on),
]