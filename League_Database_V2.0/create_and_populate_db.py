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
INSERT INTO "Team"("TeamID","SchoolName","ADPhone","ADEmail","Location")
VALUES
    (1,'Kailua High School','8081111111','adkhs@gmail.com','451 Ulumanu Drive, Kailua, HI 96734'),
    (2,'Big High School','8082222222','adbig@gmail.com','123 Drive, Kailua, HI 96734'),
    (3,'Makani High School','8083333333','admakani@gmail.com','789 Wind Ave, Honolulu, HI 96815'),
    (4,'Honu High School','8084444444','adhonu@gmail.com','321 Turtle Bay, Kaneohe, HI 96744'),
    (5,'Aloha High School','8085555555','adaloha@gmail.com','456 Lei Street, Honolulu, HI 96817');

INSERT INTO "Guardian"("GuardianID","FirstName","LastName","Phone","Email")
VALUES
    (1, 'Ella', 'Johnson', '8081234567', 'mom@gmail.com'),
    (2, 'Dwayne', 'Pebble', '8089999999', 'dad@gmail.com'),
    (3, 'Mia', 'Rivera', '8086543210', 'mia.rivera@gmail.com');

INSERT INTO "Player"("PlayerID","FirstName","LastName","DOB","Number","StartingPosition","TeamID")
VALUES
    (1, 'Penny', 'Johnson', '2004-08-21', 27, 'Striker', 1),
    (2, 'Rachel', 'Pebble', '2004-09-30', 4, 'Striker', 2);

INSERT INTO "Player_Position"("PlayerID","Position","StartDate")
VALUES
    (1, 'Striker', '2016-01-17'),
    (2, 'Striker', '2018-05-13');

INSERT INTO "Guardian_Player"("PlayerID","GuardianID","Relationship")
VALUES
    (1, 1, 'Mother'),
    (2, 2, 'Father');

INSERT INTO "Coach"("CoachID","FirstName","LastName","Phone","Email","Rank","TeamID")
VALUES
    (1, 'Richard', 'Swanson', '8082345678', 'rscoach@gmail.com','Head', 1),
    (2, 'Larry', 'Greenwood', '8084567890', 'lgcoach@gmail.com','Head', 2);

INSERT INTO "Match"("MatchID", "MatchDate", "HomeTeamID", "AwayTeamID")
VALUES
    (1, '2024-10-28', 1, 2);

INSERT INTO "Result"("ResultID", "MatchID", "WinnerID")
VALUES
    (1, 1, 1);

INSERT INTO "Score"("ScoreID", "MatchID", "PlayerID", "Goals", "Assists")
VALUES
    (1, 1, 1, 3, 1);
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
