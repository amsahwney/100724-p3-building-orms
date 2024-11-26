from lib import CONN, CURSOR
from lib.models import Book, Review # DONT FORGET TO CHANGE THESE
from lib.practice import Movie
from lib.app import App

# the code below will only run if we are running the index.py file directly      
if __name__ == "__main__":
    app = App()
    app.run()

# run this file with:
    # python -i index.py