"""
URL configuration for foodzone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views 
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('Contact/',views.Contact_us,name="Contact"),
    path('about/',views.about,name="about"),
    path('register/',views.register,name="register"),
    path('login/', views.signin, name='login'),
    path('team/',views.team_members,name="team"),
    path('dishes/',views.all_dishes,name="all_dishes"),
    path('contact/', views.contact_view, name='contact'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check_user_exists/',views.check_user_exists,name="check_user_exist"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dish/<int:id>/', views.single_dish, name='dish'),
    path('paypal/',include('paypal.standard.ipn.urls')),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('menu/', views.menu_view, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('booking/blog/', views.booking_blog, name='booking_blog'),
    path('feature/', views.feature, name='feature'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path('success/', views.success_page, name='success'),
    
    


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
