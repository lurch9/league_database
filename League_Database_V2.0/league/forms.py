from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import Team, Player, Match, Score, Profile

class AdminCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Set role as admin
            Profile.objects.create(user=user, role='admin')
        return user

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['schoolname', 'adphone', 'ademail', 'location']
        labels = {
            'schoolname': 'School Name',
            'adphone': 'Athletic Director Phone',
            'ademail': 'Athletic Director Email',
            'location': 'School Location',
        }
        widgets = {
            'schoolname': forms.TextInput(attrs={'class': 'form-control'}),
            'adphone': forms.TextInput(attrs={'class': 'form-control'}),
            'ademail': forms.EmailInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['firstname', 'lastname', 'number', 'startingposition', 'teamid']
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'number': 'Jersey Number',
            'startingposition': 'Starting Position',
            'teamid': 'Team',
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'startingposition': forms.TextInput(attrs={'class': 'form-control'}),
            'teamid': forms.Select(attrs={'class': 'form-select'}),
        }

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['matchdate', 'hometeamid', 'awayteamid']
        labels = {
            'matchdate': 'Match Date',
            'hometeamid': 'Home Team',
            'awayteamid': 'Away Team',
        }
        widgets = {
            'matchdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hometeamid': forms.Select(attrs={'class': 'form-select'}),
            'awayteamid': forms.Select(attrs={'class': 'form-select'}),
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['matchid', 'playerid', 'goals', 'assists']

    def save(self, commit=True):
        with transaction.atomic():
            instance = super().save(commit=False)
            match = instance.matchid
            player_team = instance.playerid.teamid

            if player_team == match.hometeamid:
                match.home_score += instance.goals
            elif player_team == match.awayteamid:
                match.away_score += instance.goals

            if commit:
                match.save()
                instance.save()

        return instance

