"""PGPI_GGez_314 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from GGez_App import views
from django.conf import settings
import django.views
from GGez_App.signup import Signup
from GGez_App.catalogo import Catalogo
from GGez_App.carrito import Cart
from GGez_App.login import Login, logout
from django.conf.urls.static import static
from GGez_App.views import Carrito
from GGez_App.checkOut import CheckOut


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('media/<path>', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    path('cat/', Catalogo.as_view(), name='cat'),
    path('catalogo/', views.catalogo, name='catalogo'),
    
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout , name='logout'),
    path('carrito/', views.Carrito, name='carrito'),
    path('cart/', Cart.as_view(), name='cart'),
    path('pedidos/', views.pedido, name='pedidos'),
    path('politicaEnvio/', views.politicaEnvio),
    path('checkOut/', CheckOut.as_view()),
    path('politicaPrivacidad/', views.politicaPrivacidad),
    path('atencionCliente/', views.atencionCliente),
    path('sobreNosotros/', views.datosEmpresa),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
