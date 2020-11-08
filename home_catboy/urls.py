
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<uuid:id>/',views.home, name="homecatboy"),
    path('history/<uuid:id>/', views.orderHistory, name='orderhistory'),
    path('search/<uuid:id>/', views.searchService, name='searchservice'),
    path('earnings/<uuid:id>/', views.orderEarnings, name='orderearnings'),
    path('order/<uuid:id>/',views.catboyOrder, name="catboyorder"),
    path('createorder/<uuid:id>/', views.createOrder, name='createcatboyorder'),
    path('vieworder/<uuid:id>/', views.viewCatboyOrder, name='viewcatboyorder'),
    path('vieworderlist/<uuid:id>/<uuid:oid>/', views.viewCatboyOrderList, name='viewcatboyorderlist'),
    path('vieworderaccept/<uuid:id>/<uuid:oid>/', views.viewCatboyOrderAccept, name='viewcatboyorderaccept'),
    path('ordercomplete/<uuid:id>/<uuid:cid>/<uuid:oid>/<str:date>/', views.orderComplete, name='catboyordercomplete'),
    path('accept/<uuid:id>/<uuid:cid>/<uuid:oid>/<str:date>/', views.orderAccept, name='orderaccept'),
    path('request/<uuid:cid>/<uuid:oid>/<str:date>/', views.orderRequest, name='orderrequest'),
    path('searchrequest/<uuid:cid>/<uuid:oid>/<str:date>/', views.searchOrderRequest, name='searchorderrequest'),
    path('cancel/<uuid:cid>/<uuid:oid>/<str:date>/', views.orderCancel, name='ordercancel'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)