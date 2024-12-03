import sqlite3
# Run 'python create_and_populate_db.py' in your command line to create and populate DB
DATABASE_FILE = "league_database.sqlite3"

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS "Team" (
    "TeamID" INTEGER,
    "SchoolName" TEXT,
    "ADPhone" TEXT,
    "ADEmail" TEXT,
    "Location" TEXT,
    PRIMARY KEY("TeamID")
);

CREATE TABLE IF NOT EXISTS "Guardian" (
    "GuardianID" INTEGER,
    "FirstName" TEXT,
    "LastName" TEXT,
    "Phone" TEXT,
    "Email" TEXT,
    PRIMARY KEY("GuardianID")
);

CREATE TABLE IF NOT EXISTS "Player" (
    "PlayerID" INTEGER,
    "FirstName" TEXT,
    "LastName" TEXT,
    "DOB" TEXT,
    "Number" INTEGER,
    "StartingPosition" TEXT,
    "TeamID" INTEGER,
    PRIMARY KEY("PlayerID"),
    FOREIGN KEY("TeamID") REFERENCES "Team"("TeamID")
);

CREATE TABLE IF NOT EXISTS "Player_Position" (
    "PlayerID" INTEGER,
    "Position" TEXT,
    "StartDate" TEXT,
    PRIMARY KEY("PlayerID"),
    FOREIGN KEY("PlayerID") REFERENCES "Player"("PlayerID")
);

CREATE TABLE IF NOT EXISTS "Guardian_Player" (
    "PlayerID" INTEGER,
    "GuardianID" INTEGER,
    "Relationship" TEXT,
    PRIMARY KEY("PlayerID","GuardianID"),
    FOREIGN KEY("GuardianID") REFERENCES "Guardian"("GuardianID"),
    FOREIGN KEY("PlayerID") REFERENCES "Player"("PlayerID")
);

CREATE TABLE IF NOT EXISTS "Coach" (
    "CoachID" INTEGER,
    "FirstName" TEXT,
    "LastName" TEXT,
    "Phone" TEXT,
    "Email" TEXT,
    "Rank" TEXT,
    "TeamID" INTEGER,
    PRIMARY KEY("CoachID"),
    FOREIGN KEY("TeamID") REFERENCES "Team"("TeamID")
);

CREATE TABLE IF NOT EXISTS "Coach_Position" (
    "CoachID" INTEGER,
    "Position" TEXT,
    "StartDate" TEXT,
    PRIMARY KEY("CoachID"),
    FOREIGN KEY("CoachID") REFERENCES "Coach"("CoachID")
);

CREATE TABLE IF NOT EXISTS "Match" (
    "MatchID" INTEGER,
    "MatchDate" TEXT,
    "HomeTeamID" INTEGER,
    "AwayTeamID" INTEGER,
    PRIMARY KEY("MatchID"),
    FOREIGN KEY("AwayTeamID") REFERENCES "Team"("TeamID"),
    FOREIGN KEY("HomeTeamID") REFERENCES "Team"("TeamID")
);

CREATE TABLE IF NOT EXISTS "Result" (
    "ResultID" INTEGER,
    "MatchID" INTEGER,
    "WinnerID" INTEGER,
    PRIMARY KEY("ResultID"),
    FOREIGN KEY("MatchID") REFERENCES "Match"("MatchID"),
    FOREIGN KEY("WinnerID") REFERENCES "Team"("TeamID")
);

CREATE TABLE IF NOT EXISTS "Score" (
    "ScoreID" INTEGER,
    "MatchID" INTEGER,
    "PlayerID" INTEGER,
    "Goals" INTEGER,
    "Assists" INTEGER,
    PRIMARY KEY("ScoreID"),
    FOREIGN KEY("MatchID") REFERENCES "Match"("MatchID"),
    FOREIGN KEY("PlayerID") REFERENCES "Player"("PlayerID")
);
"""


INSERT_DATA_SQL = """
INSERT OR IGNORE INTO "Team"("TeamID","SchoolName","ADPhone","ADEmail","Location")
VALUES
    (1,'Kailua High School','8081111111','adkhs@gmail.com','451 Ulumanu Drive, Kailua, HI 96734'),
    (2,'Big High School','8082222222','adbig@gmail.com','123 Drive, Kailua, HI 96734'),
    (3,'Makani High School','8083333333','admakani@gmail.com','789 Wind Ave, Honolulu, HI 96815'),
    (4,'Honu High School','8084444444','adhonu@gmail.com','321 Turtle Bay, Kaneohe, HI 96744'),
    (5,'Aloha High School','8085555555','adaloha@gmail.com','456 Lei Street, Honolulu, HI 96817'),
    (6, 'Moanalua', '8084649382', 'moanafc@gmail.com', 'Moanalua, HI'),
    (7, 'Castle', '8084738291', 'castlefc@gmail.com', 'Castle, HI'),
    (8, 'Roosevelt', '8084827164', 'rooseveltfc@gmail.com', 'Roosevelt, HI'),
    (9, 'Kahuku', '8084916283', 'kahukufc@gmail.com', 'Kahuku, HI'),
    (10, 'McKinley', '8085027483', 'mckinleyfc@gmail.com', 'McKinley, HI'),
    (11, 'Farrington', '8085138291', 'farringtonfc@gmail.com', 'Farrington, HI'),
    (12, 'Kalani', '8085248273', 'kalanifc@gmail.com', 'Kalani, HI'),
    (13, 'Kaiser', '8085348273', 'kaiserfc@gmail.com', 'Kaiser, HI'),
    (14, 'Aiea', '8085482373', 'aieafc@gmail.com', 'Aiea, HI'),
    (15, 'Waipahu', '8085527483', 'waipahufc@gmail.com', 'Waipahu, HI'),
    (16, 'Pearl City', '8085627483', 'pearlcityfc@gmail.com', 'Pearl City, HI');
INSERT OR IGNORE INTO "Guardian"("GuardianID","FirstName","LastName","Phone","Email")
VALUES
    (1, 'Ella', 'Johnson', '8081234567', 'mom@gmail.com'),
    (2, 'Dwayne', 'Pebble', '8089999999', 'dad@gmail.com'),
    (3, 'Mia', 'Rivera', '8086543210', 'mia.rivera@gmail.com');

INSERT OR IGNORE INTO "Player"("PlayerID","FirstName","LastName","DOB","Number","StartingPosition","TeamID")
VALUES
    (1, 'Penny', 'Johnson', '2004-08-21', 27, 'Striker', 1),
    (2, 'Rachel', 'Pebble', '2004-09-30', 4, 'Striker', 2),
    (3, 'Nikki', 'Tamayo', '2002-01-15', 1, 'Midfielder', 1),
    (4, 'Kylee', 'Smith', '2003-05-10', 2, 'Midfielder', 1),
    (5, 'Hilinai', 'Keeno', '2001-07-12', 3, 'Forward', 1),
    (6, 'Kassi', 'Hepfer', '2003-03-05', 6, 'Forward', 1),
    (7, 'Jadie', 'Tamaye', '2002-09-21', 7, 'Midfielder', 1),
    (8, 'Jolie', 'Woodward', '2002-11-11', 8, 'Midfielder', 1),
    (9, 'Kaena', 'Kiaaina', '2004-02-18', 9, 'Fullback', 1),
    (10, 'Reese', 'Marrotte', '2004-06-25', 11, 'Goalkeeper', 1),
    (11, 'Ashlyn', 'Nakashima', '2002-08-30', 12, 'Forward', 1),
    (12, 'Makayla', 'Lopez', '2003-10-01', 13, 'Forward', 1),
    (13, 'Kiana', 'Ching', '2001-04-17', 14, 'Defender', 1),
    (14, 'Maddie', 'DeJournett', '2002-12-03', 15, 'Defender', 1),
    (15, 'Mikaila', 'Gaspar', '2002-02-14', 16, 'Defender', 1),
    (16, 'Kiana', 'Carvalho', '2001-11-25', 17, 'Midfielder/Forward', 1),
    (17, 'Trinity', 'Wright', '2003-03-09', 18, 'Midfielder', 1),
    (18, 'Tara', 'Wright', '2003-01-21', 19, 'Defender', 1),
    (19, 'Tori', 'DeJournett', '2001-05-07', 20, 'Midfielder', 1),
    (20, 'Jordan', 'Sylva', '2004-09-14', 21, 'Forward/Midfielder', 1),
    (21, 'Mia', 'Godish-Ajolo', '2004-07-10', 22, 'Defender', 1),
    (22, 'Molly', 'Jones', '2002-06-19', 23, 'Forward/Defender', 1),
    (23, 'Khyrstin', 'Kohatsu', '2001-03-01', 24, 'Midfielder', 1);
    

INSERT OR IGNORE INTO "Player_Position"("PlayerID","Position","StartDate")
VALUES
    (1, 'Striker', '2016-01-17'),
    (2, 'Striker', '2018-05-13'),
    (3, 'Midfielder', '2018-01-15'),
    (4, 'Midfielder', '2018-05-10'),
    (5, 'Forward', '2018-07-12'),
    (6, 'Forward', '2019-03-05'),
    (7, 'Midfielder', '2019-09-21'),
    (8, 'Midfielder', '2019-11-11'),
    (9, 'Fullback', '2020-02-18'),
    (10, 'Goalkeeper', '2020-06-25');

    
    
INSERT OR IGNORE INTO "Guardian_Player"("PlayerID","GuardianID","Relationship")
VALUES
    (1, 1, 'Mother'),
    (2, 2, 'Father');

INSERT OR IGNORE INTO "Coach"("CoachID","FirstName","LastName","Phone","Email","Rank","TeamID")
VALUES
    (1, 'Richard', 'Swanson', '8082345678', 'rscoach@gmail.com','Head', 1),
    (2, 'Larry', 'Greenwood', '8084567890', 'lgcoach@gmail.com','Head', 2),
    (3, 'Michael', 'Johnson', '8082345678', 'michaeljohnson@gmail.com', 'Head', 3),
    (4, 'Sarah', 'Williams', '8083456780', 'sarahwilliams@gmail.com', 'Head', 4),
    (5, 'David', 'Brown', '8084567890', 'davidbrown@gmail.com', 'Head', 5),
    (6, 'Jessica', 'Jones', '8085678901', 'jessicajones@gmail.com', 'Head', 6),
    (7, 'James', 'Garcia', '8086789012', 'jamesgarcia@gmail.com', 'Head', 7),
    (8, 'Mary', 'Miller', '8087890123', 'marymiller@gmail.com', 'Head', 8),
    (9, 'Christopher', 'Davis', '8088901234', 'chrisdavis@gmail.com', 'Head', 9),
    (10, 'Patricia', 'Martinez', '8089012345', 'patriciamartinez@gmail.com', 'Head', 10),
    (11, 'Robert', 'Hernandez', '8080123456', 'roberthernandez@gmail.com', 'Head', 11),
    (12, 'Linda', 'Lopez', '8081234568', 'lindalopez@gmail.com', 'Head', 12),
    (13, 'William', 'Gonzalez', '8082345679', 'williamgonzalez@gmail.com', 'Head', 13),
    (14, 'Elizabeth', 'Clark', '8083456781', 'elizabethclark@gmail.com', 'Head', 14),
    (15, 'Joseph', 'Lewis', '8084567891', 'josephlewis@gmail.com', 'Head', 15),
    (16, 'Barbara', 'Walker', '8085678902', 'barbarawalker@gmail.com', 'Head', 16);

INSERT OR IGNORE INTO "Match"("MatchID", "MatchDate", "HomeTeamID", "AwayTeamID")
VALUES
    (1, '2024-10-28', 1, 2),
    (2, '2019-12-04', 1, 6),
    (3, '2019-12-07', 1, 7),
    (4, '2019-12-11', 8, 1),
    (5, '2019-12-14', 9, 1),
    (6, '2019-12-28', 1, 4),
    (7, '2020-01-04', 10, 1),
    (8, '2020-01-08', 1, 11),
    (9, '2020-01-13', 12, 1),
    (10, '2020-01-15', 1, 13),
    (11, '2020-01-21', 14, 1),
    (12, '2020-01-22', 1, 15),
    (13, '2020-01-24', 16, 1),
    (14, '2020-02-03', 1, 6),
    (15, '2023-01-15', 2, 3),
    (16, '2023-02-05', 3, 4),
    (17, '2023-02-20', 4, 5),
    (18, '2023-03-10', 5, 2),
    (19, '2023-03-25', 2, 4),
    (20, '2023-04-05', 3, 5),
    (21, '2023-04-15', 4, 2),
    (22, '2023-05-10', 5, 3),
    (23, '2023-05-25', 2, 5),
    (24, '2023-06-15', 3, 2),
    (25, '2023-07-05', 4, 3),
    (26, '2023-07-20', 5, 4),
    (27, '2023-08-10', 2, 3),
    (28, '2023-08-25', 3, 4),
    (29, '2023-09-10', 4, 5),
    (30, '2023-09-25', 5, 2),
    (31, '2023-10-10', 2, 4),
    (32, '2023-10-25', 3, 5),
    (33, '2023-11-10', 4, 2),
    (34, '2023-11-25', 5, 3);

INSERT OR IGNORE INTO "Result"("ResultID", "MatchID", "WinnerID")
VALUES
    (1, 1, 1),
    (2, 2, 1),  -- Tie
    (3, 3, 1),  -- Tie
    (4, 4, 8),
    (5, 5, 1),
    (6, 6, 1),
    (7, 7, 1),
    (8, 8, 1),
    (9, 9, 1),
    (10, 10, 1),
    (11, 11, 14),
    (12, 12, 1),  -- Won in Penalty Kick
    (13, 13, 16),
    (14, 14, 1),
    (15, 15, 2),
    (16, 16, 4),
    (17, 17, 5),
    (18, 18, NULL), -- Tie
    (19, 19, 2),
    (20, 20, 3),
    (21, 21, 2),
    (22, 22, 5),
    (23, 23, NULL), -- Tie
    (24, 24, 3),
    (25, 25, 4),
    (26, 26, 5),
    (27, 27, 2),
    (28, 28, 4),
    (29, 29, NULL), -- Tie
    (30, 30, 5),
    (31, 31, 2),
    (32, 32, 3),
    (33, 33, 4),
    (34, 34, 5);

INSERT OR IGNORE INTO "Score"("ScoreID", "MatchID", "PlayerID", "Goals", "Assists")
VALUES
    (1, 1, 1, 3, 1),
    (2, 2, 2, 1, 0),   -- Match 2, Tie, 1-1
    (3, 3, 5, 1, 0),   -- Match 3, Tie, 1-1
    (4, 4, 1, 2, 0),   -- Match 4, Roosevelt Wins 2-1
    (5, 5, 1, 3, 0),   -- Match 5, Kailua Wins 3-1
    (6, 6, 1, 4, 0),   -- Match 6, Kailua Wins 4-0
    (7, 7, 1, 8, 0),   -- Match 7, Kailua Wins 8-0
    (8, 8, 1, 9, 0),   -- Match 8, Kailua Wins 9-0
    (9, 9, 1, 4, 0),   -- Match 9, Kailua Wins 4-1
    (10, 10, 1, 3, 0), -- Match 10, Kailua Wins 3-0
    (11, 11, 1, 0, 2), -- Match 11, Aiea Wins 2-0
    (12, 12, 1, 2, 1), -- Match 12, Kailua Wins 2-1 (PK)
    (13, 13, 1, 0, 4), -- Match 13, Pearl City Wins 4-0
    (14, 14, 1, 1, 0),
    (15, 1, 23, 7, 0),   -- Khyrstin Kohatsu scored 7 goals
    (16, 1, 11, 4, 0),   -- Ashlyn Nakashima scored 4 goals
    (17, 1, 6, 3, 0),    -- Kassi Hepfer scored 3 goals
    (18, 1, 22, 2, 0),   -- Molly Jones scored 2 goals
    (19, 1, 23, 2, 0),   -- Khyrstin Kohatsu scored 2 goals
    (20, 1, 4, 2, 0),    -- Kylee Smith scored 2 goals
    (21, 1, 3, 2, 0),    -- Nikki Tamayo scored 2 goals
    (22, 15, 26, 2, 1), -- John Doe (Team 2)
    (23, 15, 34, 1, 0), -- Noah Holt (Team 3)
    -- Match 16
    (24, 16, 35, 3, 1), -- Emma Sloan (Team 3)
    (25, 16, 44, 2, 0), -- Elijah Cook (Team 4)
    -- Match 17
    (26, 17, 46, 1, 1), -- Samuel Foster (Team 4)
    (27, 17, 50, 2, 2), -- Jackson Carter (Team 5)
    -- Match 18 (Tie)
    (28, 18, 28, 1, 0), -- Liam Barker (Team 2)
    (29, 18, 53, 1, 1), -- Abigail Grimes (Team 5)
    -- Match 19
    (30, 19, 29, 2, 1), -- Sophia Everett (Team 2)
    (31, 19, 48, 1, 0), -- Logan Hayes (Team 4)
    -- Match 20
    (32, 20, 36, 3, 1), -- James Fox (Team 3)
    (33, 20, 55, 2, 0), -- Ella Fletcher (Team 5)
    (34, 21, 31, 1, 1), -- Olivia Hart (Team 2)
    (35, 21, 47, 2, 0), -- Mia Griffin (Team 4)
    -- Match 22
    (36, 22, 63, 3, 2), -- Ava Ross (Team 6)
    (37, 22, 50, 2, 1), -- Jackson Carter (Team 5)
    -- Match 23 (Tie)
    (38, 23, 33, 1, 0), -- Amelia Shaw (Team 2)
    (39, 23, 52, 1, 0), -- Owen Morgan (Team 5)
    -- Match 24
    (40, 24, 38, 3, 1), -- Aiden West (Team 3)
    (41, 24, 30, 2, 0), -- Ethan Blake (Team 2)
    (42, 25, 49, 1, 1), -- Aria Wallace (Team 4)
    (43, 25, 37, 2, 0), -- Isabella Greene (Team 3)
    -- Match 26
    (44, 26, 56, 2, 1), -- Wyatt Jenkins (Team 5)
    (45, 26, 48, 1, 0), -- Logan Hayes (Team 4)
    -- Match 27
    (46, 27, 26, 3, 2), -- John Doe (Team 2)
    (47, 27, 34, 2, 0), -- Noah Holt (Team 3)
    -- Match 28
    (48, 28, 45, 1, 1), -- Zoe Murray (Team 4)
    (49, 28, 36, 3, 0), -- James Fox (Team 3)
    -- Match 29 (Tie)
    (50, 29, 43, 2, 1), -- Lily Watson (Team 4)
    (51, 29, 57, 2, 1), -- Victoria McCoy (Team 5)
    -- Match 30
    (52, 30, 58, 1, 1), -- Oliver Bennett (Team 6)
    (53, 30, 62, 3, 0); 
"""


def main():

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    print("Creating tables...")
    cursor.executescript(CREATE_TABLES_SQL)

    print("Populating tables...")
    cursor.executescript(INSERT_DATA_SQL)

    conn.commit()
    conn.close()
    print("Database created and populated successfully.")

if __name__ == "__main__":
    main()
