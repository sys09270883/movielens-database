from django.shortcuts import render
from django.views.generic import View
from .forms import OptionForm
from .models import User, Data, MovieGenre, Genre, Movie
from django.db import connection
from django.db.models import F
from django.db.models import Count, Avg
from django.db.models import Subquery
from itertools import chain
import pymysql


class ResultView(View):
    def get(self, request):
        return render(request, 'option_select/result.html')

    def post(self, request):
        DB = 'DB_201511271'
        HOST = '127.0.0.1'
        PORT = 3306
        USER = 'yoonseop'
        PASSWORD = '1234'

        conn = pymysql.connect(host=HOST, port=PORT, db=DB, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        cursor._defer_warnings = True

        form = OptionForm(request.POST)
        genre = form['genre'].value()
        occupation = form['occupation'].value()
        vote = form['vote'].value()
        min_rating = form['min_rating'].value()
        max_rating = form['max_rating'].value()
        sorted_option = form['sorted_option'].value()

        result = []

        drop_X_query = """
        DROP TABLE IF EXISTS X;
        """

        create_X_query = """
        CREATE TEMPORARY TABLE IF NOT EXISTS X (
        mid INT PRIMARY KEY,
        genre VARCHAR(15) NOT NULL,
        UNIQUE KEY(mid)
        );
        """

        movie_genre_query = """
        INSERT IGNORE INTO X(mid, genre)
        SELECT Movie_Genre.mid, genre
        FROM Genre, Movie_Genre
        WHERE Genre.gid = Movie_Genre.gid and Movie_Genre.mid in (
        SELECT mid
        FROM Movie
        )
        """
        if genre != "all":
            movie_genre_query += "and genre = '" + genre + "'"

        drop_Y_query = """
        DROP TABLE IF EXISTS Y;
        """

        create_Y_query = """
        CREATE TEMPORARY TABLE IF NOT EXISTS Y (
        mid INT PRIMARY KEY,
        occupation VARCHAR(20),
        vote INT NOT NULL,
        rating FLOAT NOT NULL
        );
        """

        movie_user_query = """
        INSERT INTO Y(mid, occupation, vote, rating)
        SELECT Data.mid, User.occupation, COUNT(Data.mid) AS vote, AVG(Data.rating) AS rating  
        FROM User, Data
        WHERE User.uid = Data.uid and Data.mid in (
        SELECT mid
        FROM Movie
        )
        """
        if occupation != "all":
            movie_user_query += "and occupation = '" + occupation + "'"
        movie_user_query += "GROUP BY Data.mid "
        movie_user_query += "HAVING AVG(Data.rating) >= " + min_rating + " and AVG(Data.rating) <= " + max_rating
        movie_user_query += " and COUNT(Data.mid) >= " + vote

        drop_Z_query = """
        DROP TABLE IF EXISTS Z;
        """

        create_Z_query = """
        CREATE TEMPORARY TABLE IF NOT EXISTS Z (
        mid INT,
        gid INT,
        titlename VARCHAR(100),
        PRIMARY KEY(mid, gid)
        );
        """

        movie_query = """
        INSERT INTO Z(mid, gid, titlename)
        SELECT Movie_Genre.mid, Movie_Genre.gid, Movie.titlename
        FROM Movie, Movie_Genre
        WHERE Movie.mid = Movie_Genre.mid and Movie_Genre.gid in (
        SELECT gid
        FROM Genre
        )
        """

        final_query = """
        SELECT DISTINCT(X.mid), Z.titlename, X.genre, Y.occupation, Y.vote, Y.rating
        FROM X, Y, Z
        WHERE X.mid = Y.mid and Y.mid = Z.mid
        """
        if sorted_option == "rating order":
            final_query += "ORDER BY Y.rating DESC"
        elif sorted_option == "rating reverse order":
            final_query += "ORDER BY Y.rating ASC"
        elif sorted_option == "movie title order":
            final_query += "ORDER BY Z.titlename ASC"
        elif sorted_option == "movie title reverse order":
            final_query += "ORDER BY Z.titlename DESC"
        elif sorted_option == "voting order":
            final_query += "ORDER BY Y.vote DESC"
        elif sorted_option == "voting reverse order":
            final_query += "ORDER BY Y.vote ASC"

        cursor.execute(drop_X_query)
        cursor.execute(create_X_query)
        cursor.execute(movie_genre_query)
        cursor.execute(drop_Y_query)
        cursor.execute(create_Y_query)
        cursor.execute(movie_user_query)
        cursor.execute(drop_Z_query)
        cursor.execute(create_Z_query)
        cursor.execute(movie_query)
        cursor.execute(final_query)
        conn.commit()

        for line in cursor.fetchall():
            result.append(line)

        context = {
            'form': form,
            'result': result,
        }

        return render(request, 'option_select/result.html', context=context)
