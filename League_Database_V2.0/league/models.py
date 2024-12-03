# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('default', 'Default User'),
        ('guardian', 'Guardian'),
        ('coach', 'Coach'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='default')
    
# Signal to automatically create Profile for new users
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Coach(models.Model):
    coachid = models.AutoField(db_column='CoachID', primary_key=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True)  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    rank = models.TextField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    teamid = models.ForeignKey('Team', models.DO_NOTHING, db_column='TeamID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Coach'


class CoachPosition(models.Model):
    coachid = models.OneToOneField(Coach, models.DO_NOTHING, db_column='CoachID', primary_key=True)  # Field name made lowercase.
    position = models.TextField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
    startdate = models.TextField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Coach_Position'


class Guardian(models.Model):
    guardianid = models.AutoField(db_column='GuardianID', primary_key=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True)  # Field name made lowercase.
    phone = models.TextField(db_column='Phone', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Guardian'


class GuardianPlayer(models.Model):
    playerid = models.OneToOneField('Player', models.DO_NOTHING, db_column='PlayerID', primary_key=True)  # Field name made lowercase. The composite primary key (PlayerID, GuardianID) found, that is not supported. The first column is selected.
    guardianid = models.ForeignKey(Guardian, models.DO_NOTHING, db_column='GuardianID', blank=True, null=True)  # Field name made lowercase.
    relationship = models.TextField(db_column='Relationship', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Guardian_Player'


class Team(models.Model):
    teamid = models.AutoField(db_column='TeamID', primary_key=True)
    schoolname = models.TextField(db_column='SchoolName', blank=True, null=True)
    adphone = models.TextField(db_column='ADPhone', blank=True, null=True)
    ademail = models.TextField(db_column='ADEmail', blank=True, null=True)
    location = models.TextField(db_column='Location', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Team'
    def __str__(self):
        return self.schoolname or "Unnamed Team"

class Player(models.Model):
    playerid = models.AutoField(db_column='PlayerID', primary_key=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True)  # Field name made lowercase.
    dob = models.TextField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number', blank=True, null=True)  # Field name made lowercase.
    startingposition = models.TextField(db_column='StartingPosition', blank=True, null=True)  # Field name made lowercase.
    teamid = models.ForeignKey('Team', models.DO_NOTHING, db_column='TeamID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Player'


class PlayerPosition(models.Model):
    playerid = models.OneToOneField(Player, models.DO_NOTHING, db_column='PlayerID', primary_key=True)  # Field name made lowercase.
    position = models.TextField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
    startdate = models.TextField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Player_Position'


class Match(models.Model):
    matchid = models.AutoField(db_column='MatchID', primary_key=True)
    matchdate = models.TextField(db_column='MatchDate', blank=True, null=True)
    hometeamid = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="home_matches", db_column='HomeTeamID')
    awayteamid = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="away_matches", db_column='AwayTeamID')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'Match'



class Score(models.Model):
    scoreid = models.AutoField(db_column='ScoreID', primary_key=True)
    matchid = models.ForeignKey(Match, on_delete=models.CASCADE, db_column='MatchID', related_name='scores')
    playerid = models.ForeignKey('Player', on_delete=models.CASCADE, db_column='PlayerID')
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'Score'


class Result(models.Model):
    resultid = models.AutoField(db_column='ResultID', primary_key=True)  # Field name made lowercase.
    matchid = models.ForeignKey(Match, models.DO_NOTHING, db_column='MatchID', blank=True, null=True)  # Field name made lowercase.
    winnerid = models.ForeignKey('Team', models.DO_NOTHING, db_column='WinnerID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Result'