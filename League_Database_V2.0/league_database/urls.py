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
from django.contrib.auth import views as auth_views

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
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # New route for searching player by name
    path('search/', views.search_player, name='search_player'),

    # Team paths
    path('manage-teams/', views.manage_teams, name='manage_teams'),
    path('admin-panel/teams/add/', views.add_team, name='add_team'),
    path('admin-panel/teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('manage-teams/delete/<int:team_id>/', views.delete_team, name='delete_team'),

    # Player paths
    path('manage-players/', views.manage_players, name='manage_players'),
    path('manage-players/add/', views.add_player, name='add_player'),
    path('manage-players/edit/<int:player_id>/', views.edit_player, name='edit_player'),
    path('manage-players/delete/<int:player_id>/', views.delete_player, name='delete_player'),

    # Match paths
    path('manage-matches/', views.manage_matches, name='manage_matches'),
    path('manage-matches/add/', views.add_match, name='add_match'),
    path('manage-matches/edit/<int:match_id>/', views.edit_match, name='edit_match'),
    path('manage-matches/delete/<int:match_id>/', views.delete_match, name='delete_match'),

    # Score paths
    path('manage-scores/', views.manage_scores, name='manage_scores'),
    path('manage-scores/add/', views.edit_score, name='add_score'),  # Reuse edit_score for adding
    path('manage-scores/edit/<int:score_id>/', views.edit_score, name='edit_score'),
    path('manage-scores/delete/<int:score_id>/', views.delete_score, name='delete_score'),

    # Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='league/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
