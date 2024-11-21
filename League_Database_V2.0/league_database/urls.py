"""
URL configuration for league_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from league import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('teams/', views.all_teams, name='all_teams'),
    path('guardians/', views.all_guardians, name='all_guardians'),
    path('players/team/', views.players_by_team, name='players_by_team'),
    path('teams/<int:team_id>/', views.team_details, name='team_details'),
    path('team-player-count/', views.players_count_by_team, name='players_count_by_team'),
    path('team-goals/', views.team_goals, name='team_goals'),
    path('match/<int:match_id>/stats/', views.player_stats_for_match, name='player_stats_for_match'),
    path('player/<int:player_id>/stats/', views.player_stats, name='player_stats'),

]
