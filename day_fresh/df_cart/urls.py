from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$',views.cart),
    url(r'^(?P<goods_id>\d+)_(?P<count>\d+)/$',views.add),
    url(r'^goods_count/$', views.goods_count),
    url(r'^edit/(?P<goodsId>\d+)_(?P<count>\d+)/$', views.edit),
    url(r'^delete/(?P<cartId>\d+)/$',views.delete)
]