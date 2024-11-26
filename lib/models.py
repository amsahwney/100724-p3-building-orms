############## IMPORTS ##############

# the . stands for our __init__.py
from . import CONN, CURSOR


############## Book ##############

class Book:

    def __init__(self, name:str, author:str, id:int=None):
        self.id = id
        self.name = name
        self.author = author

    def __repr__(self):
        return f"Book(id={self.id}, name={self.name}, author={self.author})"

    # --- SQL CLASS METHODS --- #

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        author TEXT
        )
        """ # HEREDOC

        CONN.execute(sql)


    # creates a new instance for each row in the db
    @classmethod
    def get_all(cls):
        sql = """
        SELECT * FROM books
        """

        books_data = CURSOR.execute(sql).fetchall()

        # book_instances = []
        # for book_tuple in books_data:
        #     book = Book(id=book_tuple[0],name=book_tuple[1], author=book_tuple[2])
        #     book_instances.append(book)

        # bk is book_tuple
        book_instances = [ Book(
            id=bk[0],
            name=bk[1], 
            author=bk[2]
        ) for bk in books_data ]

        return book_instances

    # finds by id and if found instantiates a new instance
    @classmethod
    def get_by_id(cls, id:int):
        sql = """
        SELECT * FROM books
        WHERE id = ?
        """

        book_tuple = CURSOR.execute(sql, [id]).fetchone()

        if book_tuple:

            book = Book(
                id=book_tuple[0],
                name=book_tuple[1], 
                author=book_tuple[2]
            )

            return book

    # --- SQL INSTANCE METHODS --- #

    # creates in the db and updates instance with the new id
    def create(self):
        sql = """
        INSERT INTO books (name, author)
        VALUES (?, ?)
        """

        CURSOR.execute(sql, [self.name, self.author])
        CONN.commit()

        last_row_sql = """
        SELECT id FROM books
        ORDER BY id DESC
        LIMIT 1
        """

        self.id = CURSOR.execute(last_row_sql).fetchone()[0]

        return self

    # updates the row based on current attributes 
    def update(self):
        sql = """
        UPDATE books
        SET name = ?, author = ?
        WHERE id = ?
        """

        CURSOR.execute(sql, [self.name, self.author, self.id])
        CONN.commit()

        return self

    # creates or updates depending on whether item exists in db
    def save(self):
        if self.id:
            self.update()
        else:
            self.create()
        return self
        
    
    # deletes the instance from the db and removes the id
    def destroy(self):
        sql = """
        DELETE FROM books
        WHERE id = ?
        """

        CURSOR.execute(sql, [self.id])
        CONN.commit()

        self.id = None


    # --- JOIN METHODS --- #

    # return a list of instances of each student
    def reviews(self):
        sql = """
        SELECT * FROM reviews
        WHERE book_id = ?
        """

        review_tuples = CURSOR.execute(sql, [self.id]).fetchall()

        review_instances = [ Review(
            id=rv[0], 
            stars=rv[1], 
            username=rv[2], 
            book_id=rv[3]
        ) for rv in review_tuples ]

        return review_instances


############## END Book ##############



############## Review ##############

class Review:

    def __init__(self, stars:int, username:str, book_id:int, id:int=None):
        self.id = id
        self.stars = stars
        self.username = username
        self.book_id = book_id

    def __repr__(self):
        return f'Review(id={self.id}, stars={self.stars}, username={self.username}, book_id={self.book_id})'
    

    # --- CLASS SQL METHODS --- #

    # make a table if it doesn't exist
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        stars INTEGER,
        username TEXT,
        book_id INTEGER
        )
        """

        CONN.execute(sql)


    # --- SQL METHODS --- #

    def create(self):
        sql = """
        INSERT INTO reviews (stars, username, book_id)
        VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, [self.stars, self.username, self.book_id])
        CONN.commit()

        last_row_sql = """
        SELECT id FROM reviews
        ORDER BY id DESC
        LIMIT 1
        """

        self.id = CURSOR.execute(last_row_sql).fetchone()[0]

        return self
        # add to the database

    def update(self):
        sql = """
        UPDATE reviews
        SET stars = ?, username = ?, book_id = ?
        WHERE id = ?
        """

        CURSOR.execute(sql, [self.stars, self.username, self.book_id, self.id])
        CONN.commit()

        return self
        # update based on current instance attributes

    # creates or updates depending on whether item exists in db
    def save(self):
        if self.id:
            self.update()
        else:
            self.create()
        return self

    # remove from the database
    # deletes the instance from the db and removes the id
    def destroy(self):
        sql = """
        DELETE FROM reviews
        WHERE id = ?
        """

        CURSOR.execute(sql, [self.id])
        CONN.commit()

        self.id = None
        # destroy row in the db based on id


    # --- SQL CLASS METHODS --- #

    @classmethod
    def get_by_id(cls, id):
        sql = """
        SELECT * FROM reviews
        WHERE id = ?
        """

        rv_tuple = CURSOR.execute(sql, [id]).fetchone()

        if rv_tuple:

            review = Review(
                id=rv_tuple[0],
                stars=rv_tuple[1], 
                username=rv_tuple[2],
                book_id=rv_tuple[3]
            )

            return review
    
    @classmethod
    def get_all(cls):
        sql = """
        SELECT * FROM reviews
        """

        review_data = CURSOR.execute(sql).fetchall()

        review_instances = [ Review(
            id=rv[0],
            stars=rv[1], 
            username=rv[2],
            book_id=rv[3]
        ) for rv in review_data ]

        return review_instances
        # return all instances from the database


    # --- JOIN METHODS --- #

    def book(self):
        return Book.get_by_id(self.book_id)


############## END Review ##############