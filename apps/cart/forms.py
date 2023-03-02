from django import forms


class CheckoutForm(forms.Form):
    promo_code = forms.CharField(max_length=20, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form__input mr--20 mr-xs--0',
                                                               'placeholder': 'Промокод'}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    house = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    building = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    apartment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))

    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form__input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form__input', }))

    description = forms.CharField(required=False, max_length=2014)
