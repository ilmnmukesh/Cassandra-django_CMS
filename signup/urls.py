
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.SignupMain, name="signup"),
    path('catboy/',views.SignupCatBoy, name="signupcatboy"),
    path('catering/',views.SignupCatering, name="signupcat"),
    path('customer/',views.SignupCust, name="signupcust"),
    path('mahal/',views.SignupMahal, name="signupmahal"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)