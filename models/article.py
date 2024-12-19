from database.connection import get_db_connection

class Article:
    def __init__(self, title, content, author_id, magazine_id, id = None):
        if not isinstance(title, str):
            raise TypeError("Title must be of type string")
        if not (5 <= len(title) <= 50):
            raise ValueError ("Title must be between 5 and 50 characters.")
        
        if not isinstance(content, str):
            raise TypeError("Content must be of type string")
        if (len(content) == 0):
            raise ValueError ("Content must be more than 0 characters")

        if not isinstance (author_id, int) or not isinstance (magazine_id, int):
            raise TypeError("Author ID and Magazine ID must be of type integer")
        
        
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._id = id or self._insert_article()


    def _insert_article(self):
        """Insert the article into the database and retrieve its ID."""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
            """,
            (self._title, self._content, self._author_id, self._magazine_id)
        )    
        connection.commit()

        article_id = cursor.lastrowid
        connection.close()
        return article_id
    
    def _update_database(self, column, value):
        """Updates a specific column in the database"""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            f"UPDATE articles SET {column} = ? WHERE id = ? ",
            (value, self._id),
        )
        connection.commit()
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title    
    
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content (self, new_content):
        if not isinstance (new_content, str) or len(new_content) == 0:
            raise ValueError("Content must be a non-empty string")
        self._content = new_content
        self._update_database("content", new_content)

    @property
    def author(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT authors.id, authors.name
            FROM authors WHERE authors.id = ?
            """,
            (self._author_id,)
        )    
        author = cursor.fetchone()
        connection.close()

        if author:
            return Author(author[1], author[0])
        return None
    
    @property
    def magazine(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magaines WHERE magazines.id = ?
            """,
            (self._magazine_id,)
        )
        magazine = cursor.fetchone()
        connection.close()

        if magazine:
            return Magazine(magazine[1], magazine[2],magazine[0])
        return None

    def __repr__(self):
        return f'<Article {self.title}>'
