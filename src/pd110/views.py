from django.shortcuts import render

# Create your views here. def es una funcion (def 'nombrefunction')
def about(request):
    return render(request, "about.html", {})
