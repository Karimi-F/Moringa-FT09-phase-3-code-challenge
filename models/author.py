import sqlite3
from database.connection import get_db_connection


class Author:
    def __init__(self, name, id = None):
        if not isinstance (name, str):
            raise TypeError("Name must be of type string")
        if (len(name) == 0):
            raise ValueError ("Name must be more than 0 characters")

        self._id = id or self._create_author()
        self.name = name

        self._create_author()


    def _create_author(self):
        """Insert the author into the database and retrieve its ID."""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute ("INSERT INTO authors (name) VALUES (?)", (self._name,))
        connection.commit()

        author_id = cursor.lastrowid
        connection.close()
        if not isinstance(author_id, int):
            raise ValueError("Database returned an invalid ID")
        return author_id

    @property
    def id(self):
        """Getter for ID."""
        return self._id    
    
    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify the author's ID")
        # if not isinstance(value, int):
        #     raise TypeError ("ID must be of type integer.")
        
        # self._id = value
    
    @property
    def name(self):
        """Getter for Name."""
        return self._name
    
    @name.setter
    def name (self, value):
        """Cannot modify name after creation."""
        if hasattr(self, "_name"):
            raise AttributeError("Cannot set the author's name after instantiation.")
        if not isinstance (value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def articles(self):
        connection = get_db_connection()    
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT articles.id, articles.title, articles.content, articles.magazine_id         
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
            """,
            (self._id,)
        )
        articles = cursor.fetchall()
        connection.close()
        return articles
    
    def magazines (self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """,
            (self._id,)
        )
        magazines = cursor.fetchall()
        connection.close()
        return magazines

    def __repr__(self):
        return f'<Author {self.name}>'
