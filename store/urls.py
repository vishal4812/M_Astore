from django.urls import path
from . import views


app_name='store'

urlpatterns = [
    
    path('',views.HomeView.as_view(),name='Homeview'),
    path('product/<slug>/',views.ProductView.as_view(),name='product'),
    path('order-summary/',views.OrderSummaryView.as_view(),name='order-summary'),
    path('add_to_cart/<slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>',views.remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('blog/',views.blog,name='blog'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('handlerequest/', views.handlerequest, name="Handlerequest"),
    path('search/',views.search,name='Search'),
    path('header/',views.header,name='header')
]