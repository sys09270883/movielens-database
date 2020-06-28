import _tsv_parser
import _create_tables
import pymysql
import datetime

data, genre, item, occupation, user = _tsv_parser.parse()
DB = 'DB_201511271'
HOST = '127.0.0.1'
PORT = 3306
USER = 'yoonseop'
PASSWORD = '1234'

conn = pymysql.connect(host=HOST, port=PORT, db=DB, user=USER, password=PASSWORD)
cursor = conn.cursor()
cursor._defer_warnings = True


def create_table():
    queries = _create_tables.makeQuery()
    for query in queries:
        cursor.execute(query)
    conn.commit()
    print(" # Create table")


def insert_data():
    qry = "INSERT IGNORE INTO `Data`(`uid`, `mid`, `rating`, `timestamp`) VALUES (%s, %s, %s, %s)"
    data_list = []
    for line in data.iterrows():
        uid = int(line[1][0])
        mid = int(line[1][1])
        rating = int(line[1][2])
        timestamp = datetime.datetime.fromtimestamp(int(line[1][3])).strftime('%Y-%m-%d %H:%M:%S')
        data_list.append((uid, mid, rating, timestamp))
    cursor.executemany(qry, data_list)
    conn.commit()
    print(" # Insert data")


def insert_user():
    qry = "INSERT IGNORE INTO `User`(`uid`, `age`, `gender`, `occupation`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
    user_list = []
    for line in user.iterrows():
        user_list.append((line[1][0], line[1][1], line[1][2], line[1][3], line[1][4]))
    cursor.executemany(qry, user_list)
    conn.commit()
    print(" # Insert user")


def insert_genre():
    qry = "INSERT IGNORE INTO `Genre`(`gid`, `genre`) VALUES (%s, %s)"
    genre_list = []

    for line in genre.iterrows():
        genre_list.append((line[1][1], line[1][0]))
    cursor.executemany(qry, genre_list)
    conn.commit()
    print(" # Insert genre")


def insert_movie():
    movie_qry = "INSERT IGNORE INTO `Movie`(`mid`, `titleName`, `releaseDate`, `IMDbUrl`) VALUES (%s, %s, %s, %s)"
    movie_list = []
    genre_qry = "INSERT IGNORE INTO `Movie_Genre`(`gid`, `mid`) VALUES (%s, %s)"
    genre_list = []
    movie_idx = 1

    for line in item.iterrows():
        mid = int(line[1][0])
        title_name = str(line[1][1])
        release_date = str(line[1][2])
        if release_date == 'nan':
            release_date = '27-Sep-1996'
        imdb_url = str(line[1][4])
        if imdb_url == 'nan':
            imdb_url = 'null'
        release_date = datetime.datetime.strptime(release_date, '%d-%b-%Y')
        movie_list.append((mid, title_name, release_date, imdb_url))

        for i in range(5, len(line[1])):
            if line[1][i] == 1:
                genre_list.append((i - 5, movie_idx))
        movie_idx += 1

    cursor.executemany(movie_qry, movie_list)
    cursor.executemany(genre_qry, genre_list)
    conn.commit()
    print(" # Insert movie")


create_table()
insert_user()
insert_genre()
insert_movie()
insert_data()


cursor.close()
conn.close()
