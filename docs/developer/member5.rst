Parts Implemented by Sefa Eren Şahin
====================================

**Players, Teams and Squad tables are implemented.**

**Players Table**

Table is created by following sql code::

   code-block:: python
   CREATE TABLE IF NOT EXISTS PLAYERS
                       ( PLAYER_ID serial NOT NULL PRIMARY KEY,
                         NAME varchar(100) NOT NULL,
                         BIRTHDAY date NOT NULL,
                         POSITION varchar(100) NOT NULL
                       )

asd

