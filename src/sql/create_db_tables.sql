----------------------------
-- Initialize all db tables
-----------------------------

--Create players table
CREATE TABLE "Players" (
	"Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Name" TEXT NOT NULL UNIQUE,
	"IsActive" INTEGER NOT NULL DEFAULT 1
);


--Create games table
CREATE TABLE "Games" (
	"Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Name" TEXT NOT NULL UNIQUE,
	"Developer" TEXT,
	"Platform" TEXT,
	"ReleaseYear" INTEGER,
	"IsActive" INTEGER NOT NULL DEFAULT 1
);


--Create records table
CREATE TABLE "MatchRecords" (
	"Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"GameId" INTEGER NOT NULL,
	"Player1Id" INTEGER NOT NULL,
	"Player2Id" INTEGER NOT NULL,
	"WinnerId" INTEGER NOT NULL,
	"Date" DATETIME NOT NULL,
	FOREIGN KEY("GameId") REFERENCES "Games"("Id"),
	FOREIGN KEY("Player1Id") REFERENCES "Players"("Id"),
	FOREIGN KEY("Player2Id") REFERENCES "Players"("Id"),
	FOREIGN KEY("WinnerId") REFERENCES "Players"("Id")
);
