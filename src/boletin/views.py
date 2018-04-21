from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import RegModelForm, ContactForm, BuscarForm
from .models import Registrado


# Create your views here. def es una funcion (def 'nombrefunction')
def inicio(request):
    titulo = "Bienvenidos"
    form2 = BuscarForm(request.POST or None)
    
    if request.user.is_authenticated():
        titulo = "Bienvenido %s" %(request.user)
    form = RegModelForm(request.POST or None)#none es para q no muestre el mensaje de campo obligatorio 
    
    context = {
        "titulo": titulo,
        "el_form": form,
        "el_form2": form2,
    }
    
    if form.is_valid():
        instance = form.save(commit=False)
        nombre = form.cleaned_data.get("nombre")
        email = form.cleaned_data.get("email")
        if not instance.nombre:
            instance.nombre = "PERSONA"
        instance.save()

        context = {
            "titulo": "Gracias %s!" %(nombre)
        }
        
        if not nombre:
            context = {
                "titulo": "Gracias persona sin nombre !!"
            }

        print instance
        print instance.timestamp

        #form_data = form.cleaned_data
        #abc = form_data.get("email")
        #abc2 = form_data.get("nombre")
        #obj = Registrado.objects.create(email=abc, nombre=abc2)
    if request.user.is_authenticated() and request.user.is_staff:
        if form2.is_valid():
            form_data = form2.cleaned_data
            buscar = form_data.get("buscar")
            queryset = Registrado.objects.all().order_by("-timestamp").filter(nombre__icontains=buscar)
        else:
            queryset = Registrado.objects.all().order_by("-timestamp")
        # i = 1
        # for instance in Registrado.objects.all():
        #     print(i)
        #     print(instance)
        #     print(instance.nombre)
        #     i +=1
        
        context = {
            'queryset' : queryset ,
            'el_form2' : form2,
        }
    return render(request, "inicio.html", context)

def contact(request):
    titulo = "Contacto"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # primera forma 
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        # segunda forma
        # for key in form.cleaned_data:
        #     print key
        #     print form.cleaned_data.get(key)
        # tercera forma
        form_email =  form.cleaned_data.get("email")
        form_mensaje = form.cleaned_data.get("mensaje")
        form_nombre = form.cleaned_data.get("nombre")
        asunto = 'From de contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email_from, "dflondono26@misena.edu.co"]
        email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)
        send_mail(asunto,
            email_mensaje,
            email_from,
            email_to,
            fail_silently=False
        )
        # print email, mensaje, nombre
    context = {
        "form": form,
        'titulo': titulo,
    }
    return render(request, "forms.html", context)
