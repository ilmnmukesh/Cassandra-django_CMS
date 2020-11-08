
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('catering/<uuid:id>/',views.editCatering, name="editcatering"),
    path('catboy/<uuid:id>/',views.editCatboy, name="editcatboy"),
    path('customer/<uuid:id>/',views.editCustomer, name="editcustomer"),
    path('mahal/<uuid:id>/',views.editMahal, name="editmahal"),
    path('editdetails/<str:service>/<uuid:id>/', views.editDetails, name="editdetails"),
    path('editemail/<str:service>/<uuid:id>/', views.editEmail, name="editemail"),
    path('editcontact/<str:service>/<uuid:id>/', views.editContact, name="editcontact"),
    path('editpassword/<str:service>/<uuid:id>/', views.editPassword, name="editpassword"),
    path('editpicture/<str:service>/<uuid:id>/', views.editPicture, name="editpicture"),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)