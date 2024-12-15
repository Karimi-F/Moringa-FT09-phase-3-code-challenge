from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if not isinstance(title, str):
            raise TypeError("Title must be of type string")
        if not (5 <= len(title) <= 50):
            raise ValueError ("Title must be between 5 and 50 characters.")
        
        if not isinstance (author_id, int) or not isinstance (magazine_id, int):
            raise TypeError("Author ID and Magazine ID must be of type integer")
        
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

        self._insert_article()

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

        self._id = cursor.lastrowid
        connection.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title    

    def __repr__(self):
        return f'<Article {self.title}>'
