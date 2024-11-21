from django.shortcuts import render
from django.shortcuts import render
from django.db import connection

def homepage(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.TeamID, t.SchoolName,
                   SUM(CASE WHEN t.TeamID = r.WinnerID THEN 1 ELSE 0 END) AS Wins,
                   SUM(CASE WHEN t.TeamID <> r.WinnerID AND (m.HomeTeamID = t.TeamID OR m.AwayTeamID = t.TeamID) THEN 1 ELSE 0 END) AS Losses,
                   CAST(SUM(CASE WHEN t.TeamID = r.WinnerID THEN 1 ELSE 0 END) AS FLOAT) /
                   NULLIF(SUM(CASE WHEN t.TeamID = r.WinnerID OR t.TeamID <> r.WinnerID THEN 1 ELSE 0 END), 0) AS WinPercentage
            FROM Team t
            LEFT JOIN Match m ON t.TeamID = m.HomeTeamID OR t.TeamID = m.AwayTeamID
            LEFT JOIN Result r ON m.MatchID = r.MatchID
            GROUP BY t.TeamID, t.SchoolName
            ORDER BY Wins DESC, Losses ASC
        """)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        team_rankings = [dict(zip(columns, row)) for row in rows]
    return render(request, 'league/homepage.html', {'team_rankings': team_rankings})




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

def players_by_team(request):
    team_name = request.GET.get('team_name', '')  # Get the team name from the query parameters
    players = []

    if team_name:  # Only execute the query if a team name is provided
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.*
                FROM Player p
                JOIN Team t ON p.TeamID = t.TeamID
                WHERE t.SchoolName LIKE %s
            """, [f"%{team_name}%"])  # Use SQL LIKE for partial matching
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            players = [dict(zip(columns, row)) for row in rows]

    return render(request, 'league/players_by_team.html', {'players': players, 'team_name': team_name})


def players_count_by_team(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.SchoolName AS TeamName, COUNT(p.PlayerID) AS PlayerCount
            FROM Team t
            LEFT JOIN Player p ON t.TeamID = p.TeamID
            GROUP BY t.SchoolName
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

def team_details(request, team_id):
    with connection.cursor() as cursor:
        # Fetch team details
        cursor.execute("SELECT * FROM Team WHERE TeamID = %s", [team_id])
        team = cursor.fetchone()
        team_columns = [col[0] for col in cursor.description]
        team_data = dict(zip(team_columns, team)) if team else None

        # Fetch players for the team, excluding DOB
        cursor.execute("""
            SELECT FirstName, LastName, Number, StartingPosition
            FROM Player
            WHERE TeamID = %s
        """, [team_id])
        players = cursor.fetchall()
        player_columns = [col[0] for col in cursor.description]
        player_data = [dict(zip(player_columns, player)) for player in players]

        # Fetch matches involving the team
        cursor.execute("""
            SELECT m.MatchID, m.MatchDate, ht.SchoolName AS HomeTeam, at.SchoolName AS AwayTeam
            FROM Match m
            JOIN Team ht ON m.HomeTeamID = ht.TeamID
            JOIN Team at ON m.AwayTeamID = at.TeamID
            WHERE m.HomeTeamID = %s OR m.AwayTeamID = %s
        """, [team_id, team_id])
        matches = cursor.fetchall()
        match_columns = [col[0] for col in cursor.description]
        match_data = [dict(zip(match_columns, match)) for match in matches]

    return render(request, 'league/team_details.html', {
        'team': team_data,
        'players': player_data,
        'matches': match_data,
    })


