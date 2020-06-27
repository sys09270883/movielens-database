from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Option


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ['genre', 'occupation', 'min_rating', 'max_rating', 'sorted_option']
