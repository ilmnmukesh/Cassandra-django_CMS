
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<uuid:id>/',views.home, name="homecatering"),
    path('order/<uuid:id>/',views.order, name="cateringorder"),
    path('createorder/<uuid:id>/', views.createOrder, name='createcateringorder'),
    path('gallery/<uuid:id>/', views.gallery, name='cateringgallery' ),
    path('add/gallery/<uuid:id>/', views.addgallery, name='addgallerycatering'),
    path('delete/gallery/<uuid:id>/<int:pos>/', views.delete, name='deletegallerycatering'),

    path('add/foodlist/<uuid:id>/', views.foodList, name='createfoodlist'),
    path('view/orderlist/<uuid:id>/', views.viewOrder, name='viewcateringorder'),
    path('view/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.viewServiceOrder, name='viewcateringrequest'),
    path('accept/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.acceptRequest, name='acceptcateringrequest'),
    path('cancel/order/<uuid:id>/<uuid:cid>/<str:type>/<str:date>/', views.cancelRequest, name='cancelcateringrequest'),
    
    path('view/catboy/request/<uuid:id>/<uuid:oid>/', views.viewCatboyrequest, name="viewcatboyrequestbycatering"),
    path('accept/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.acceptCatboyrequest, name="acceptcatboyrequestbycatering"),
    path('complete/catboy/request/<uuid:id>/<uuid:oid>/<uuid:cid>/<str:date>/', views.completeCatboyrequest, name="completecatboyrequestbycatering"),

    path('history/<uuid:id>/', views.history, name='cateringhistory'),
    path('earning/<uuid:id>/', views.earnings, name='cateringearning'),
    path('search/<uuid:id>/', views.searchCatboyList, name='searchcatboybycatering'),
    path('view/<uuid:id>/', views.viewCatboyList, name='viewcatboybycatering'),

    path('add/food/morning/<uuid:id>/', views.addBreakfast, name='addvegfoodmrng'),
    path('add/food/afternon/veg/<uuid:id>/', views.addLunchVeg, name='addvegfoodafn'),
    path('add/food/afternon/non/<uuid:id>/', views.addLunchNonVeg, name='addnonfoodafn'),    
    path('add/food/night/veg/<uuid:id>/', views.addDinnerVeg, name='addvegfoodnyt'),
    path('add/food/nigth/non/<uuid:id>/', views.addDinnerNonVeg, name='addnonfoodnyt'),

    path('delete/food/morning/<uuid:id>/<str:value>/', views.deleteBreakfast, name='deletevegfoodmrng'),
    path('delete/food/veg/afternoon/<uuid:id>/<str:value>/', views.deleteLunchVeg, name='deletevegfoodafn'),
    path('delete/food/non/afternoon/<uuid:id>/<str:value>/', views.deleteLunchNonVeg, name='deletenonfoodafn'),
    path('delete/food/veg/dinner/<uuid:id>/<str:value>/', views.deleteDinnerVeg, name='deletevegfoodnyt'),
    path('delete/food/non/dinner/<uuid:id>/<str:value>/', views.deleteDinnerNonVeg, name='deletenonfoodnyt'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)