from django.shortcuts import render
from django.views.generic import View
from .forms import OptionForm
from django.db import connection
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
        titlename VARCHAR(100) NOT NULL,
        UNIQUE KEY(mid)
        );
        """

        movie_genre_query = """
        INSERT IGNORE INTO X(mid, genre, titlename)
        SELECT Movie.mid, Genre.genre, Movie.titlename
        FROM Genre, Movie
        WHERE Genre.mid = Movie.mid
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

        final_query = """
        SELECT DISTINCT(X.mid), X.titlename, X.genre, Y.occupation, Y.vote, Y.rating
        FROM X, Y
        WHERE X.mid = Y.mid
        """
        if sorted_option == "rating order":
            final_query += "ORDER BY Y.rating DESC"
        elif sorted_option == "rating reverse order":
            final_query += "ORDER BY Y.rating ASC"
        elif sorted_option == "movie title order":
            final_query += "ORDER BY X.titlename ASC"
        elif sorted_option == "movie title reverse order":
            final_query += "ORDER BY X.titlename DESC"
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
        cursor.execute(final_query)
        conn.commit()

        for line in cursor.fetchall():
            result.append(line)

        context = {
            'form': form,
            'result': result,
        }

        return render(request, 'option_select/result.html', context=context)
