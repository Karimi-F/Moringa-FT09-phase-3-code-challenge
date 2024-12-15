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
            self.create_magazine()    

    def create_magazine(self):
        """Insert the magazine and retrieves its ID."""
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO magazines(name, category) VALUES (?, ?)",
            (self._name, self._category)
        )
        connection.commit()

        self._id = cursor.lastrowid
        connection.close()

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

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE magazine SET category = ? WHERE id = ?" ,
            (self._category, self._id)
        )
        connection.commit()
        connection.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'
