from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('patient_data/', views.add_patient_data,name='patient_data'),
    path('delete_patient/<int:patient_id>/', views.delete_patient_data, name='delete_patient'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
