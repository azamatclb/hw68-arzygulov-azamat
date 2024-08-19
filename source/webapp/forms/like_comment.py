from django import forms


class CommentLikeForm(forms.Form):
    comment_id = forms.IntegerField(widget=forms.HiddenInput())
