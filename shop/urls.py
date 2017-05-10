from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v1/login/$', views.Login.as_view(), name='login'),
    url(r'^api/v1/register/$', views.Register.as_view(), name='register'),
    url(r'^api/v1/items/$', views.ShopItemsList.as_view(), name='register'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
]
