from django import forms

from Comics.models import *


class ComicDownloadsForm(forms.Form):
    url = forms.CharField()
    link = forms.ModelChoiceField(
        queryset=Website.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link'].label = ''
        self.fields['link'].required = False
        self.fields['url'].required = True
        self.fields['url'].label = 'Website Link'
        self.fields['url'].widget.attrs.update(
            {'class': 'form-control'})
