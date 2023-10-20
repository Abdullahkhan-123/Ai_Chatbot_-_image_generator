from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.chatbot, name='chatbot'),
    # path('login/', views.login, name='login'),
    # path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # this side is my urls i am abdullah khan
    path('', views.chatpage, name='chatbot'),
    path('img_gen/', views.img_gen, name='img_gen'),
    path('logins/', views.log, name='log'),
    path('registers/', views.reg, name='reg'),
    path('chatpage/', views.chatpage, name='chatpage'),

    


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)