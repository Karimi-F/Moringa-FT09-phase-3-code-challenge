import sqlite3
from database.connection import get_db_connection


class Author:
    def __init__(self, id, name):
        if not isinstance (name, str)  or len(name) == 0:
            raise TypeError("Name must be of type string")
        if (len(name) == 0):
            raise ValueError ("Name must be more than 0 characters")

        self.id = id
        self.name = name

        self.create_author()


    def create_author(self):
        """Insert the author into the database and retrieve its ID."""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute ("INSERT INTO authors (name) VALUES (?)", (self._name,))
        connection.commit()

        self._id = cursor.lastrowid
        connection.close()

    @property
    def id(self):
        """Getter for ID."""
        return self._id    
    
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError ("ID must be of type integer.")
        
        self._id = value
    
    @property
    def name(self):
        """Getter for Name."""
        return self._name
    
    @name.setter
    def name (self, value):
        """Cannot modify name after creation."""
        if hasattr(self, "_name"):
            raise AttributeError("Cannot set the author's name after instantiation.")
        
        self._name = value

    def __repr__(self):
        return f'<Author {self.name}>'
