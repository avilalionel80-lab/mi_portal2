from django import forms


class LoginForm(forms.Form):
    dni = forms.CharField(
<<<<<<< HEAD
        label="DNI",
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "Ingresa tu DNI",
            "autocomplete": "off",
        }),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "Ingresa tu email",
            "autocomplete": "off",
        }),
    )
    remember_me = forms.BooleanField(
        label="Recordarme",
        required=False,
    )
    terms = forms.BooleanField(
        label="Acepto los términos y condiciones",
        required=True,
        error_messages={"required": "Debés aceptar los términos y condiciones para continuar."},
    )

    def clean_dni(self):
        # Normalizamos el DNI quitando espacios y puntos.
        return self.cleaned_data["dni"].strip().replace(".", "")
=======
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
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
