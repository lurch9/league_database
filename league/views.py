from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("<h1>Welcome to the League Database</h1><p>Navigate to <a href='/teams/'>Teams</a> or <a href='/guardians/'>Guardians</a></p>")


def all_teams(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Team")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        teams = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/all_teams.html', {'teams': teams})

def all_guardians(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Guardian")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        guardians = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/all_guardians.html', {'guardians': guardians})

def players_by_team(request, team_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Player WHERE TeamID = %s", [team_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        players = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/players_by_team.html', {'players': players, 'team_id': team_id})

def players_count_by_team(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TeamID, COUNT(PlayerID) AS PlayerCount
            FROM Player
            GROUP BY TeamID
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        team_counts = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/players_count_by_team.html', {'team_counts': team_counts})

def team_goals(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.SchoolName, SUM(s.Goals) AS TotalGoals
            FROM Team t
            JOIN Player p ON t.TeamID = p.TeamID
            JOIN Score s ON p.PlayerID = s.PlayerID
            GROUP BY t.SchoolName
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        team_goals = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/team_goals.html', {'team_goals': team_goals})

def player_stats_for_match(request, match_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.FirstName, p.LastName, s.Goals, s.Assists
            FROM Player p
            JOIN Score s ON p.PlayerID = s.PlayerID
            WHERE s.MatchID = %s
        """, [match_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        stats = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/player_stats_for_match.html', {'stats': stats, 'match_id': match_id})

