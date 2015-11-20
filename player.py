class Player:
    def __init__(self, id, name, teamid, age, kitno):
        self.id = id
        self.name = name
        self.teamid = teamid
        self.age = age
        self.kitno = kitno

'''
    tablo sql kodu

    CREATE TABLE PLAYERS
    (
    ID INTEGER PRIMARY KEY,
    NAME VARCHAR(50) NOT NULL,
    TEAMID INTEGER REFERENCES TEAMS(ID),
    AGE INTEGER NOT NULL,
    KITNO INTEGER
    )
'''