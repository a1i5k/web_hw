"""askme_zhuravlev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='new'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('question/<int:pk>/', views.one_question, name='question'),
    path('signup/', views.register, name='signup'),
    path('vote/', views.vote, name='vote'),
    path('vote_current/', views.vote_correct, name='vote'),
    path('vote_answer/', views.vote_answer, name='vote'),
    path('<pk>/settings/', views.settings, name='settings'),
    path('tag/<pk>', views.tag, name='tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
