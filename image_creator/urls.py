"""
URL configuration for image_creator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from image_generator.views import generate_image



def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('generate')
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root_redirect'),
    path('generate/', login_required(generate_image), name='generate'),
    path('image_generator/', include('image_generator.urls')),
    path('hydrogen_arts/', include('hydrogen_arts.urls')),
    path('user/', include('User.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
