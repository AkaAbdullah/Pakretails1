from django.contrib import admin
from django.urls import path
from mainpage import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from mainpage.forms import myLoginForm, myPasswordChangeForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signupuser,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(),name='productdetail'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentmethod/',views.paymentmethod,name='paymentmethod'),
    path('orders/',views.orders,name='orders'),
    path('loginuser/',auth_views.LoginView.as_view(template_name='mainpage/login.html',authentication_form=myLoginForm),name='login_user'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='mainpage/passwordchange.html',form_class=myPasswordChangeForm,success_url='/profile/'),name='passwordchange'),
    path('cart/',views.show_cart,name='show_cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('about/',views.about,name='about'),
    path('feedback/',views.FeedbackView.as_view(),name='feedback'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "PAKRETAILS"
admin.site.site_title = "PAKRETAILS Admin Portal"
admin.site.index_title = "Welcome to PAKRETAILS Portal"