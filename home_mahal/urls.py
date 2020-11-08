
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<uuid:id>/',views.home, name="homemahal"),
    path('create/catboy/<uuid:id>/', views.catboyOrder, name='createcatboybymahal'),
    path('create/catboy/order/<uuid:id>/', views.createCatboyOrderByMahal, name='createcatboyorderbymahal'),
    
    path('search/catboy/<uuid:id>/',views.searchListCatboy, name="mahalsearchcatboy"),
    path('search/catering/<uuid:id>/',views.searchListCatering, name="mahalsearchcatering"),
    
    path('view/catboy/<uuid:id>/',views.viewCatboy, name="mahalviewcatboy"),
    path('view/catering/<uuid:id>/',views.viewCatering, name="mahalviewcatering"),

    path('user/catboy/<uuid:id>/<uuid:cid>/', views.viewCatboyUser, name="viewcatboyuserbymahal"),
    path('user/catering/booking/<uuid:id>/<uuid:cid>/', views.bookCatering, name="bookcateringbymahal"),
    path('user/catering/booked/<uuid:id>/<uuid:cid>/', views.bookOrder, name="mahalbookcatering"),

    path('view/our/order/<uuid:id>/<uuid:cid>/<str:fdate>/<str:tdate>/', views.viewOurOrder, name='viewcustomerorderbymahal'),
    path('status/our/order/<uuid:id>/<uuid:cid>/<str:fdate>/<str:tdate>/<str:status>/', views.updateOurOrder, name='statuscustomerorderbymahal'),

    path('view/catering/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.viewServiceOrder, name='viewcateringrequestbymahal'),
    path('complete/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.completeCateringRequest, name='completecateringrequestbymahal'),
    path('cancel/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.cancelCateringRequest, name='cancelcateringrequestbymahal'),

    path('calendar/<uuid:id>/', views.calendar, name='mahalcalendar'),
    path('block/calendar/<uuid:id>/', views.blockCalendar, name='mahalblockcalendar'),

    path('view/order/<uuid:id>/', views.viewOrder, name='viewmahalorder'),   
    path('update/rent/<uuid:id>/', views.rentUpdate, name='mahalrentupdate'),   
    path('history/<uuid:id>/', views.history, name='mahalhistory'),   
    path('earning/<uuid:id>/', views.earning, name='mahalearning'),   


    path('user/catering/<uuid:id>/<uuid:cid>/', views.viewCateringUser, name="viewcateringuserbymahal"),
    path('view/catboy/request/<uuid:id>/<uuid:oid>/', views.viewCatboyrequest, name="viewcatboyrequestbymahal"),
    path('accept/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.acceptCatboyrequest, name="acceptcatboyrequestbymahal"),
    path('complete/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.completeCatboyrequest, name="completecatboyrequestbymahal"),

    path('gallery/<uuid:id>/', views.gallery, name='mahalgallery' ),
    path('add/gallery/<uuid:id>/', views.addgallery, name='addgallerymahal'),
    path('delete/gallery/<uuid:id>/<int:pos>/', views.delete, name='deletegallerymahal'),

    path('add/cart/catering/<uuid:id>/<uuid:cid>/<str:type>/<str:name>/<int:rate>/<int:count>/<str:veg>/', views.addToCart,name='addtocartcatering'),
    path('delete/cart/catering/<uuid:id>/<uuid:cid>/<str:type>/<str:name>/', views.deleteToCart,name='deletetocartcatering'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)