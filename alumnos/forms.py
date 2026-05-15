from django import forms


class LoginForm(forms.Form):
    dni = forms.CharField(
        label='DNI',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu DNI',
            'autocomplete': 'off',
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa tu email',
            'autocomplete': 'off',
        })
    )
    remember_me = forms.BooleanField(
        label='Recordarme',
        required=False,
        widget=forms.CheckboxInput()
    )
