from django import forms


class LoginForm(forms.Form):
    dni = forms.CharField(
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
