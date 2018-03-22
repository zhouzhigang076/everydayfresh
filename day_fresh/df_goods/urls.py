from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list/(?P<num>\d+)/$',views.list),
    url(r'^(?P<id>\d+)/$',views.detail),
]