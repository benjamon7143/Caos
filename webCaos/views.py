from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as login_aut

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contacto(request):
    return render(request, 'contacto.html')

def login(request): 
    contexto={'mensaje':''}
    if request.POST:
        usua = request.POST.get("txtusu")
        pas = request.POST.get("txtPass")
        us =  authenticate(request,username=usua,password=pas)
        if us is not None and us.is_active:
            login_aut(request,us)
            return render(request,"index.html")
        contexto={'mensaje':'usuario incorrecto'} 
    return render(request, 'login.html', contexto)

def cerrar_sesion(request):
    logout(request)
    return render(request,"index.html")

def registro(request):
    contexto={'mensaje':''}
    if request.POST:
        usua=request.POST.get("txtusuario")
        email=request.POST.get("txtEmail")
        password=request.POST.get("txtcontraseña")
        usu = User()
        usu.username=usua
        usu.email=email
        usu.set_password(password)
        try:
            usu.save()
            contexto['mensaje']='Usuario registrado'
        except:
         contexto['mensaje']='Usuario no registrado'
            
    return render(request,'login.html', contexto)
    
def sobre_nosotros(request):
    return render(request, 'sobre-nosotros.html')

def subir_noticia(request):
    cate=Categoria.objects.all()
    print(request.user.username)
    # nombre_user=request.user.username
    # use=User.objects.get(username=nombre_user)
    # print(use)
    noticia=Noticia.objects.all()
    periodistas=Periodista.objects.all()
    contexto={"Noticias":noticia,"Categoria":cate,"Periodistas":periodistas}
    if request.POST:

        titulo = request.POST.get("txtTitulo")
        descripcion = request.POST.get("txtDesc")
        fecha = request.POST.get("txtFecha")
        cat = request.POST.get("cboCategoria")
        objcat = Categoria.objects.get(IDCate = cat)
        perio = request.POST.get("cboPeriodista")
        objperio= Periodista.objects.get(IDPer = perio)
        imagen = request.FILES.get("txtIMG")
        noti = Noticia(
            Titulo=titulo,
            Descrip=descripcion,
            Fecha=fecha,
            categoria=objcat,
            periodista=objperio,
            Foto=imagen)
        noti.save()
        contexto["Mensaje"]="Enviado"
    return render(request, 'subir-noticia.html',contexto)

def admin_noticias(request):
    cate=Categoria.objects.all()
    noticia=Noticia.objects.all()
    contexto={"Noticias":noticia,"Categoria":cate}
    return render(request, 'admin-noticias.html', contexto)

def noticia_pandemia(request):
    return render(request, 'noticia-pandemia.html')

def noticia_Uchile(request):
    return render(request, 'noticia-Udechile.html')

def galeria(request):
    noticias = Noticia.objects.filter(Publicado=True)
    cantidad = Noticia.objects.filter(Publicado=True).count()
    contex = {"Noticias":noticias,'cantidad':cantidad}

    return render(request,'galeria.html',contex)
 
def Buscar_Palabra(request):
    palabra = request.POST.get('txtDesc')
    noticia = Noticia.objects.filter(Descrip__contains=palabra)
    cantidad = Noticia.objects.filter(Descrip__contains=palabra).count()
    contex={"Noticias":noticia,'cantidad':cantidad}

    return render(request,'galeria.html',contex)

def Buscar_Categoria(request,id):

    cat = request.POST.get(id)
    cate = Categoria.objects.get(NombreCate= cat)
    noticias = Noticia.objects.filter(categoria=cate)
    contex={"Noticias":noticias}

    return render(request,'galeria.html',contex)

def Buscar(request):
    palabra = request.GET.get('txtbuscar')
    resultado = Noticia.objects.filter(Descrip__contains=palabra)
    contex={"Noticias":resultado}

    return render(request,'buscador.html',contex)

def Buscador(request):

    return render(request,'buscador.html')