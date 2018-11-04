from django import forms

class PostUpdates(forms.Form):
   text = forms.CharField(max_length = 100)
   image = file = forms.FileField()