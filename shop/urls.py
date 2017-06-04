import rest_framework.authtoken.views
from django.conf.urls import url

from main import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^api/v1/login/$', rest_framework.authtoken.views.obtain_auth_token),
    url(r'^api/v1/register/$', views.Register.as_view(), name='register'),
    url(r'^api/v1/items/$', views.ShopItemsList.as_view(), name='register'),
    url(r'^api/v1/packaging/$', views.PackagingList.as_view(), name='register'),
    url(r'^api/v1/manufacturers/$', views.ManufacturerList.as_view(), name='register'),
    url(r'^api/v1/designations/$', views.DesignationList.as_view(), name='register'),
    url(r'^api/v1/cart/$', views.CartView.as_view(), name='get_cart'),
    url(r'^api/v1/cart/add/$', views.AddToCart.as_view(), name='add_cart'),
    url(r'^api/v1/cart/remove/$', views.RemoveFromCart.as_view(), name='remove_cart'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    url(r'^.*$', views.index, name='index'),
]
