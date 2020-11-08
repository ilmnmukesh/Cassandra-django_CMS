
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<uuid:id>/',views.home, name="homecustomer"),
    path('search/<uuid:id>/',views.search, name="customersearch"),
    path('search/<uuid:id>/catboy/',views.searchListCatboy, name="customersearchcatboy"),
    path('search/<uuid:id>/catering/',views.searchListCatering, name="customersearchcatering"),
    path('search/<uuid:id>/mahal/',views.searchListMahal, name="customersearchmahal"),
    path('view/catboy/<uuid:id>/',views.viewCatboy, name="viewcatboy"),
    path('view/mahal/<uuid:id>/',views.viewMahal, name="viewmahal"),
    path('view/catering/<uuid:id>/',views.viewCatering, name="viewcatering"),

    path('createorder/<uuid:id>/', views.createOrder, name='createcateringorderbycustomer'),
    path('view/order/<uuid:id>/', views.viewOrder, name='vieworderbycustomer'),

    path('history/<uuid:id>/', views.history, name='customerhistory'),

    path('view/catboy/request/<uuid:id>/<uuid:oid>/', views.viewCatboyrequest, name="viewcatboyrequestbycustomer"),
    path('accept/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.acceptCatboyrequest, name="acceptcatboyrequestbycustomer"),
    path('complete/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.completeCatboyrequest, name="completecatboyrequestbycustomer"),

    path('view/our/order/<uuid:id>/<uuid:cid>/<str:fdate>/<str:tdate>/', views.viewOurOrder, name='viewcustomerorderbycustomer'),
    path('status/our/order/<uuid:id>/<uuid:cid>/<str:fdate>/<str:tdate>/<str:status>/', views.updateOurOrder, name='statuscustomerorderbycustomer'),

    path('view/catering/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.viewServiceOrder, name='viewcateringrequestbycustomer'),
    path('complete/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.completeCateringRequest, name='completecateringrequestbycustomer'),
    path('cancel/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.cancelCateringRequest, name='cancelcateringrequestbycustomer'),
    
    path('user/catering/<uuid:id>/<uuid:cid>/', views.viewCateringUser, name="viewcateringuserbycustomer"),
    path('user/catboy/<uuid:id>/<uuid:cid>/', views.viewCatboyUser, name="viewcatboyuserbycustomer"),
    path('user/catering/booking/<uuid:id>/<uuid:cid>/', views.bookCatering, name="bookcateringbycustomer"),
    path('user/catering/booked/<uuid:id>/<uuid:cid>/', views.bookOrder, name="customerbookcatering"),

    path('delete/catering/<uuid:id>/<uuid:cid>/', views.deleteTemp, name="deletecustomertemp"),

    path('user/mahal/view/<uuid:id>/<uuid:cid>/', views.viewMahalUser, name="viewmahalbycustomer"),
    path('user/mahal/booking/<uuid:id>/<uuid:cid>/', views.bookMahal, name="bookmahalbycustomer"),

    path('add/cart/catering/<uuid:id>/<uuid:cid>/<str:type>/<str:name>/<int:rate>/<int:count>/<str:veg>/', views.addToCart,name='addtocartcustomer'),
    path('delete/cart/catering/<uuid:id>/<uuid:cid>/<str:type>/<str:name>/', views.deleteToCart,name='deletetocartcustomer'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)