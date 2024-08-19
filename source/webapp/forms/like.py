from django import forms


class ArticleLikeForm(forms.Form):
    article_id = forms.IntegerField(widget=forms.HiddenInput())
