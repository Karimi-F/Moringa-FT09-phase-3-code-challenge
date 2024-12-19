from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category, id = None):

        if not isinstance(name, str):
            raise TypeError("Name must be of type string")
        if not (2 <= len(name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        
        if not isinstance(category, str):
            raise TypeError("Category must be of type string")
        if (len(category) == 0):
            raise ValueError("Category must be longer than 0 characters")

        
        self._name = name
        self._category = category

        if id:
            self._id = id
        else:
            self._id = self._create_magazine()    

    def _create_magazine(self):
        """Insert the magazine and retrieves its ID."""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO magazines(name, category) VALUES (?, ?)",
            (self._name, self._category)
        )
        connection.commit()

        magazine_id = cursor.lastrowid
        connection.close()
        return magazine_id

    # def _update_database(self, column, value):
    #     """Update a specific column in the database"""
    #     connection = get_db_connection()
    #     cursor = connection.cursor()    

    #     cursor.execute(
    #         f"UPDATE magazine SET {column} =  ? WHERE id = ?",
    #         (value, self._id)
    #     )
    #     connection.commit()
    #     connection.close()

    @property
    def id(self):
        """Getter for ID."""
        return self._id 

    @property 
    def name(self):
        """Getter for name."""
        return self._name

    @name.setter
    def name (self, new_name):
        """Setter for name."""
        if not isinstance (new_name, str):
            raise TypeError("Name must be of type string")
        if not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        
        self._name = new_name
        # self._update_database("name", self._name)


        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE magazines SET name = ? WHERE id = ?",
            (self._name, self._id)
        )
        connection.commit()
        connection.close()

    @property
    def category (self):
        """Getter for category."""
        return self._category

    @category.setter   
    def category(self, new_category):
        """Setter for category""" 
        if not isinstance(new_category, str):
            raise TypeError("Category must be of type string")
        if (len(new_category) == 0):
            raise ValueError("Category must be longer than 0 characters")
        self._category = new_category
        # self._update_database("category, self._category")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE magazine SET category = ? WHERE id = ?" ,
            (self._category, self._id)
        )
        connection.commit()
        connection.close()

    def articles (self):
        connection = get_db_connection()
        cursor = connection.cursor()   
        cursor.execute(
            """
            SELECT articles.id, articles.title, articles.content, articles.author_id
            FROM articles
            WHERE articles.magazine_id = ?
            """,
            (self._id,)
        ) 
        articles = cursor.fetchall()
        connection.close()
        return articles
    
    def contributors (self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            """,
            (self._id,)
        )
        contributors = cursor.fetchall()
        connection.close()
        return contributors
    
    def article_titles(self):
        articles = self.articles()
        if articles:
            return [articles[1] for article in articles]
        return None
    
    def contributing_authors(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT (articles.id) > 2
            """,
            (self._id,)
        )
        contributing_authors = cursor.fetchall()
        connection.close()

        if contributing_authors:
            return contributing_authors
        return None

    def __repr__(self):
        return f'<Magazine {self.name}>'
