Developer Guide
===============

Database Design
---------------

Main purpose of this database is creating a web application to hold basic information about American Football.

Our database mainly contains information about Teams, Players, Coaches, Matches, Leagues etc.

Teams and Players tables are the most active tables. Tables like Player Statistics, Team Statistics, Transfers, Fixture are designed to keep the relations
between Teams and Players. Teams and Players tables are referenced by other tables alot.

Countries, Players, Officials, and Seasons tables are core tables. These entities do not reference any other table.

PostgreSQL is the relational database management system used in Database Design.

Psycopg2 is used as database adapter.

.. figure:: images/er.png
   :scale: 100 %
   :alt: map to buried treasure

   ER Relation Diagram of American Football Database

Code
----

**explain the technical structure of your code**

**to include a code listing, use the following example**::

   .. code-block:: python

      class Foo:

         def __init__(self, x):
            self.x = x

.. toctree::
   :maxdepth: 2

   member1
   member2
   member3
   member4
   member5
