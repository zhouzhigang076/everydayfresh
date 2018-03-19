from django.conf.urls import url,include
import views

urlpatterns = [
   url(r'^register/$',views.register),
   url(r'^register_handle/$',views.register_handle),
   url(r'^login/$',views.login),
   # url(r'^login_handle/$',views.login_handle),
   url(r'^uname_check/$',views.uname_check),
   url(r'^uemail_check/$',views.uemail_check),
   url(r'^user_center/$',views.user_center),
   url(r'^user_order/$', views.user_order),
   url(r'^user_adress/$', views.user_adress),
]