from django import forms
from django.forms import TextInput

from .models import *
from django.utils.translation import ugettext_lazy as _


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        labels = {
            'name': _('Stanowisko: ')
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Stanowisko'}),
        }

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('position_id', 'user_id', 'bio', 'picture')
        labels = {
            'position_id': _('Stanowisko: '),
            'bio': _('Twój opis: '),
            'picture': _('Twoje zdjęcie: ')
        }
        widgets = {
            'bio': TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        if 'user_id' in kwargs:
            print(kwargs)
            self.user_id = kwargs.pop('user_id')
        super(CandidateForm, self).__init__(*args, **kwargs)

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'