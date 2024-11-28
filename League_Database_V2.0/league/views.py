from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from .forms import TeamForm, PlayerForm, MatchForm, ScoreForm
from .models import Team, Player, Match, Score
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure user is not an admin by default
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'league/signup.html', {'form': form})

@login_required
def default_dashboard(request):
    if request.user.profile.role != 'default':
        return redirect('home')  # Redirect unauthorized users

    teams = Team.objects.all()  # Default users can view teams
    players = Player.objects.all().values('firstname', 'lastname', 'teamid')  # Restrict player data

    return render(request, 'league/default_dashboard.html', {
        'teams': teams,
        'players': players,
    })

# Helper function to check if user is admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return redirect('admin_panel')
    else:
        form = UserCreationForm()
    return render(request, 'league/create_admin.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'league/admin_panel.html')

# CRUD for Team
@login_required
@user_passes_test(is_admin)
def manage_teams(request):
    teams = Team.objects.all()
    print(teams)
    return render(request, 'league/manage_teams.html', {'teams': teams})

@login_required
@user_passes_test(is_admin)
def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_teams')
    else:
        form = TeamForm()
    return render(request, 'league/edit_team.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('manage_teams')
    else:
        form = TeamForm(instance=team)
    return render(request, 'league/edit_team.html', {'form': form, 'team': team})

@login_required
@user_passes_test(is_admin)
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('manage_teams')
    return render(request, 'league/confirm_delete.html', {'team': team})

# CRUD for Player
@login_required
@user_passes_test(is_admin)
def manage_players(request):
    players = Player.objects.all()
    return render(request, 'league/manage_players.html', {'players': players})

@login_required
@user_passes_test(is_admin)
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_players')
    else:
        form = PlayerForm()
    return render(request, 'league/edit_player.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('manage_players')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'league/edit_player.html', {'form': form, 'player': player})

@login_required
@user_passes_test(is_admin)
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('manage_players')
    return render(request, 'league/confirm_delete.html', {'player': player})

# CRUD for Match
@login_required
@user_passes_test(is_admin)
def manage_matches(request):
    matches = Match.objects.all()
    return render(request, 'league/manage_matches.html', {'matches': matches})

@login_required
@user_passes_test(is_admin)
def add_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_matches')
    else:
        form = MatchForm()
    return render(request, 'league/edit_match.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('manage_matches')
    else:
        form = MatchForm(instance=match)
    return render(request, 'league/edit_match.html', {'form': form, 'match': match})

@login_required
@user_passes_test(is_admin)
def delete_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        match.delete()
        return redirect('manage_matches')
    return render(request, 'league/confirm_delete.html', {'match': match})

# CRUD for Score
@login_required
@user_passes_test(is_admin)
def manage_scores(request):
    scores = Match.objects.all()  # Assuming Match model has `home_score` and `away_score` fields
    return render(request, 'league/manage_scores.html', {'scores': scores})

@login_required
@user_passes_test(is_admin)
def add_score(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_scores')
    else:
        form = ScoreForm()
    return render(request, 'league/edit_score.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_score(request, score_id=None):
    if score_id:
        score = get_object_or_404(Score, pk=score_id)
    else:
        score = None

    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            score = form.save()

            # Update the match score logic here, if necessary
            match = score.matchid
            match.home_score = Score.objects.filter(matchid=match, playerid__teamid=match.hometeamid).aggregate(total_goals=Sum('goals'))['total_goals'] or 0
            match.away_score = Score.objects.filter(matchid=match, playerid__teamid=match.awayteamid).aggregate(total_goals=Sum('goals'))['total_goals'] or 0
            match.save()

            return redirect('manage_scores')
    else:
        form = ScoreForm(instance=score)

    return render(request, 'league/edit_score.html', {'form': form, 'score': score})


@login_required
@user_passes_test(is_admin)
def delete_score(request, score_id):
    score = get_object_or_404(Score, pk=score_id)
    if request.method == 'POST':
        score.delete()
        return redirect('manage_scores')
    return render(request, 'league/confirm_delete.html', {'score': score})



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

        # Fetch players for the team, ensuring PlayerID is included
        cursor.execute("""
            SELECT PlayerID, FirstName, LastName, Number, StartingPosition
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

def player_stats(request, player_id):
    with connection.cursor() as cursor:
        # Fetch player's overall stats
        cursor.execute("""
            SELECT p.FirstName, p.LastName,
                   SUM(s.Goals) AS TotalGoals,
                   SUM(s.Assists) AS TotalAssists
            FROM Player p
            LEFT JOIN Score s ON p.PlayerID = s.PlayerID
            WHERE p.PlayerID = %s
            GROUP BY p.FirstName, p.LastName
        """, [player_id])
        player_stats = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        player_data = dict(zip(columns, player_stats)) if player_stats else None

    return render(request, 'league/player_stats.html', {'player': player_data})




