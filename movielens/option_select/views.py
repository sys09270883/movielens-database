from django.shortcuts import render
from django.views.generic import View
from .forms import OptionForm
from .models import User, Data, MovieGenre, Genre, Movie
from django.db import connection
from django.db.models import F


class ResultView(View):
    def get(self, request):
        return render(request, 'option_select/result.html')

    def post(self, request):
        form = OptionForm(request.POST)
        genre = form['genre'].value()
        occupation = form['occupation'].value()
        min_rating = form['min_rating'].value()
        max_rating = form['max_rating'].value()
        sorted_option = form['sorted_option'].value()

        result = MovieGenre.objects.select_related().annotate(
            titlename=F('mid__titlename'), genre=F('gid__genre')
        )


        context = {
            'form': form,
            'result': result,
        }

        return render(request, 'option_select/result.html', context=context)
