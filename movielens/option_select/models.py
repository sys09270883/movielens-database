from django.db import models


class Data(models.Model):
    mid = models.OneToOneField('Movie', models.DO_NOTHING, db_column='mid', primary_key=True, related_name="related_mid_uid")
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    rating = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data'
        unique_together = (('mid', 'uid'), ('mid', 'uid'),)


class Genre(models.Model):
    gid = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'genre'


class Movie(models.Model):
    mid = models.IntegerField(primary_key=True)
    titlename = models.CharField(db_column='titleName', max_length=100)  # Field name made lowercase.
    releasedate = models.DateField(db_column='releaseDate')  # Field name made lowercase.
    imdburl = models.CharField(db_column='IMDbUrl', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'movie'


class MovieGenre(models.Model):
    gid = models.OneToOneField(Genre, models.DO_NOTHING, db_column='gid', primary_key=True)
    mid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='mid', related_name="related_mid_gid")

    class Meta:
        managed = False
        db_table = 'movie_genre'
        unique_together = (('gid', 'mid'), ('gid', 'mid'),)


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=2)
    occupation = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'user'


class Option(models.Model):
    genre = models.CharField(max_length=15)
    occupation = models.CharField(max_length=15)
    vote = models.IntegerField()
    min_rating = models.FloatField()
    max_rating = models.FloatField()
    sorted_option = models.CharField(max_length=30)