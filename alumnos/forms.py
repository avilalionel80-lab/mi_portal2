from django import forms


class LoginForm(forms.Form):
    """Formulario para autenticación de alumnos con opción de recordarme."""
    
    dni = forms.CharField(
        label='DNI',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 12345678',
            'required': 'required',
            'autocomplete': 'off'
        })
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'alumno@ipf.edu.ar',
            'required': 'required',
            'autocomplete': 'off'
        })
    )
    
    remember_me = forms.BooleanField(
        label='Recordar este dispositivo',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'remember-checkbox'
        })
    )
