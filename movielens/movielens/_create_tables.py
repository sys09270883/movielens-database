import _tsv_parser as tp
import pymysql


def makeQuery():
    queries = ["""
        CREATE TABLE IF NOT EXISTS `Movie` (
            `mid`	INT	NOT NULL PRIMARY KEY,
            `titleName`	VARCHAR(100)	NOT NULL,
            `releaseDate`	DATE	NOT NULL,
            `IMDbUrl`	VARCHAR(150)	NOT NULL,
            UNIQUE KEY(`mid`)
        );
    """, """
        CREATE TABLE IF NOT EXISTS `User` (
            `uid`	INT	NOT NULL PRIMARY KEY,
            `age`	INT	NOT NULL,
            `gender`	CHAR(2)	NOT NULL,
            `occupation`   VARCHAR(15) NOT NULL,
            `zipcode`	CHAR(5)	NOT NULL,
            UNIQUE KEY(`uid`)
        );
    """, """
        CREATE TABLE IF NOT EXISTS `Genre` (
            `mid`	INT	NOT NULL,
            `genre`	VARCHAR(20)	NOT NULL,
            PRIMARY KEY(`mid`, `genre`),
            FOREIGN KEY(`mid`) REFERENCES `Movie`(`mid`)
                ON UPDATE CASCADE,
            UNIQUE KEY(`mid`, `genre`)
        );
    """, """
        CREATE TABLE IF NOT EXISTS `Data` (
            `uid`	INT	NOT NULL,
            `mid`	INT	NOT NULL,
            `rating`	INT	NOT NULL,
            `timestamp`	TIMESTAMP	NOT NULL,
            PRIMARY KEY(`uid`, `mid`),
            FOREIGN KEY(`uid`) REFERENCES `User`(`uid`)
                ON UPDATE CASCADE,
            FOREIGN KEY(`mid`) REFERENCES `Movie`(`mid`)
                ON UPDATE CASCADE,
            UNIQUE KEY(`uid`, `mid`)
        );
    """]
    return queries