from django import forms

from .models import Registrado

class RegModelForm(forms.ModelForm):
    class Meta:
        model = Registrado
        fields = ["nombre", "email"]
    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_base, proveedor = email.split("@")
        dominio, extencion = proveedor.split(".")
        if not extencion == "edu":
            raise forms.ValidationError("Por favor utiliza un email con la extencion .EDU")
        return email
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        #validaciones
        return nombre

class ContactForm(forms.Form):
    nombre = forms.CharField(required=False)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

class BuscarForm(forms.Form):
    buscar = forms.CharField(label="Buscar", required=False, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu nombre...'}))