class Team:
    def __init__(self, id, name, year, standing, avgfan):
        self.id = id
        self.name = name
        self.year = year
        self.standing = standing
        self.avgfan = avgfan

'''
    tablo sql kodu

    CREATE TABLE TEAMS
    (
    ID INTEGER PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    YEAR INTEGER NOT NULL,
    STANDING INTEGER,
    AVGFAN FLOAT
    )

'''