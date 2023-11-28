from django import forms 
from .models import *


class eventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description', 'date', 'time','location','slots_available']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
          }
    def __init__(self, *args, **kwargs):
        super(eventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['slots_available'].widget.attrs['class'] = 'form-control'
