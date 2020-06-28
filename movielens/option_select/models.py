from django.db import models


class Option(models.Model):
    genre = models.CharField(max_length=15)
    occupation = models.CharField(max_length=15)
    vote = models.IntegerField()
    min_rating = models.FloatField()
    max_rating = models.FloatField()
    sorted_option = models.CharField(max_length=30)