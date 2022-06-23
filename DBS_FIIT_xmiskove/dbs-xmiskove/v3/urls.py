from django.urls import path
from . import views

urlpatterns = [
    path('matches/<match_id>/top_purchases/',views.function1),
    path('abilities/<ability_id>/usage/',views.function2),
    path('statistics/tower_kills/',views.function3)
]