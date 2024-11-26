from lib.models import Book, Review
from time import sleep

gator = """
           .-._   _ _ _ _ _ _ _ _
.-''-.__.-'00  '-' ' ' ' ' ' ' ' '-.
'.___ '    .   .--_'-' '-' '-' _'-' '._
 V: V 'vv-'   '_   '.       .'  _..' '.'.
   '=.____.=_.--'   :_.__.__:_   '.   : :
           (((____.-'        '-.  /   : :
                             (((-'\ .' /
                           _____..'  .'
                          '-._____.-'
    """

class App:
    def __init__(self):
        Book.create_table()
        Review.create_table()
        self.input = None

    def run(self):
        cat = """
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  
        """

        print(cat)
        print("Welcome to Book Club")
        self.main_menu()

    def main_menu(self):
        printed_options = """
        1. Review a book
        2. Look up a book
        3. Exit
        """

        print(printed_options)

        while self.input not in ["1", "2", "3"]:

            self.input = input(">>> ")

            if self.input == "1":
                self.add_review()
                sleep(2)
                print(printed_options)
            elif self.input == "2":
                self.look_up() 
                sleep(2)
                print(printed_options)
            elif self.input == "3":
                self.exit_program()
            else:
                print("Hey, that's not on the menu! Please choose a number based on the menu options")

    def add_review(self):
        print("Select a book to review:")
        
        books_list = Book.get_all()
        index = 1
        for book in books_list:
            print(f"{index}. {book.name} by {book.author}")
            index += 1 

        while self.input not in range(1, len(books_list) + 1):
            try:
                self.input = int( input(">>> ") )
                if self.input in range(1, len(books_list) + 1):
                    chosen_book = books_list[self.input - 1]
                else: 
                    print("Invalid book choice, try again!")
            except:
                print("Invalid book choice, try again!")

        self.add_review_to_book(chosen_book)

    def add_review_to_book(self, book):
        print(f"You chose {book.name} by {book.author}!")

        print("How many stars would you rate this book out of 5?")
        self.input = None
        while self.input not in ["1","2","3","4","5"]:
            self.input = input(">>> ")
            if self.input  in ["1","2","3","4","5"]:
                stars = self.input
            else:
                print("Invalid star input what the heck, try again!")

        print("What is your username (5 - 15 characters)")
        self.input = None
        while not self.input or not (5 <= len(self.input) <= 15):
            self.input = input(">>> ")
            if self.input or not (5 <= len(self.input) <= 15):
                username = self.input
            else: 
                print("Invalid username...")

        print(stars, username)
        new_review = Review(stars = stars, username = username, book_id = book.id)
        new_review.save()

        print("You review has been saved!")

        self.input = None

    def exit_program(self):
        print("See ya later alligator")
        print(gator)
        exit()

    def look_up(self):
        books_list = Book.get_all()
        print("Choose a book to inspect!")

        index = 1
        for book in books_list:
            print(f"{index}. {book.name} by {book.author}")
            index += 1 

        while self.input not in range(1, len(books_list) + 1):
            try:
                self.input = int( input(">>> ") )
                if self.input in range(1, len(books_list) + 1):
                    chosen_book = books_list[self.input - 1]
                else: 
                    print("Invalid book choice, try again!")
            except:
                print("Invalid book choice, try again!")

        reviews = chosen_book.reviews()

        print(f"{book.name} by {book.author}")
        print("Reviews:")

        for rev in reviews:
            print(f"{rev.stars} - {rev.username}")


        
    

