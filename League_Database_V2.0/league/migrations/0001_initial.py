# Generated by Django 5.1.3 on 2024-11-28 00:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('coachid', models.AutoField(db_column='CoachID', primary_key=True, serialize=False)),
                ('firstname', models.TextField(blank=True, db_column='FirstName', null=True)),
                ('lastname', models.TextField(blank=True, db_column='LastName', null=True)),
                ('phone', models.TextField(blank=True, db_column='Phone', null=True)),
                ('email', models.TextField(blank=True, db_column='Email', null=True)),
                ('rank', models.TextField(blank=True, db_column='Rank', null=True)),
            ],
            options={
                'db_table': 'Coach',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('guardianid', models.AutoField(db_column='GuardianID', primary_key=True, serialize=False)),
                ('firstname', models.TextField(blank=True, db_column='FirstName', null=True)),
                ('lastname', models.TextField(blank=True, db_column='LastName', null=True)),
                ('phone', models.TextField(blank=True, db_column='Phone', null=True)),
                ('email', models.TextField(blank=True, db_column='Email', null=True)),
            ],
            options={
                'db_table': 'Guardian',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerid', models.AutoField(db_column='PlayerID', primary_key=True, serialize=False)),
                ('firstname', models.TextField(blank=True, db_column='FirstName', null=True)),
                ('lastname', models.TextField(blank=True, db_column='LastName', null=True)),
                ('dob', models.TextField(blank=True, db_column='DOB', null=True)),
                ('number', models.IntegerField(blank=True, db_column='Number', null=True)),
                ('startingposition', models.TextField(blank=True, db_column='StartingPosition', null=True)),
            ],
            options={
                'db_table': 'Player',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('matchid', models.AutoField(db_column='MatchID', primary_key=True, serialize=False)),
                ('matchdate', models.TextField(blank=True, db_column='MatchDate', null=True)),
            ],
            options={
                'db_table': 'Match',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('resultid', models.AutoField(db_column='ResultID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('scoreid', models.AutoField(db_column='ScoreID', primary_key=True, serialize=False)),
                ('goals', models.IntegerField(blank=True, db_column='Goals', null=True)),
                ('assists', models.IntegerField(blank=True, db_column='Assists', null=True)),
            ],
            options={
                'db_table': 'Score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamid', models.AutoField(db_column='TeamID', primary_key=True, serialize=False)),
                ('schoolname', models.TextField(blank=True, db_column='SchoolName', null=True)),
                ('adphone', models.TextField(blank=True, db_column='ADPhone', null=True)),
                ('ademail', models.TextField(blank=True, db_column='ADEmail', null=True)),
                ('location', models.TextField(blank=True, db_column='Location', null=True)),
            ],
            options={
                'db_table': 'Team',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoachPosition',
            fields=[
                ('coachid', models.OneToOneField(db_column='CoachID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='league.coach')),
                ('position', models.TextField(blank=True, db_column='Position', null=True)),
                ('startdate', models.TextField(blank=True, db_column='StartDate', null=True)),
            ],
            options={
                'db_table': 'Coach_Position',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuardianPlayer',
            fields=[
                ('playerid', models.OneToOneField(db_column='PlayerID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='league.player')),
                ('relationship', models.TextField(blank=True, db_column='Relationship', null=True)),
            ],
            options={
                'db_table': 'Guardian_Player',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerPosition',
            fields=[
                ('playerid', models.OneToOneField(db_column='PlayerID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='league.player')),
                ('position', models.TextField(blank=True, db_column='Position', null=True)),
                ('startdate', models.TextField(blank=True, db_column='StartDate', null=True)),
            ],
            options={
                'db_table': 'Player_Position',
                'managed': False,
            },
        ),
    ]
