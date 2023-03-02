from django import forms

from apps.blog.models import Post


class CreateCommentForm(forms.Form):
    comment = forms.CharField(max_length=512, widget=forms.Textarea(
        attrs={'class': 'form__input form__input--textarea',
               'placeholder': 'Текст комментария...'}))


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField()
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form__input'}))
    content = forms.CharField(max_length=8196, widget=forms.Textarea(
        attrs={'class': 'form__input form__input--textarea'}))

    class Meta:
        model = Post
        fields = ('image', 'title', 'content')
