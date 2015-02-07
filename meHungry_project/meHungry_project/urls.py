from django.conf.urls import patterns, include, url
from meHungry_customer_website.views import *
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from ajax_select import urls as ajax_select_urls


from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:


                       url(r'^$', homepage_view, name='homepage_view'),
                       url(r'^about/', about, name='about'),

                       # url(r'^blog/', include('blog.urls')),



                       url('', include('django.contrib.auth.urls', namespace='auth')),

                      # include the lookup urls
                       url(r'^admin/lookups/', include(ajax_select_urls)),

                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^accounts/login/', login),

                       url(r'^accounts/logout', logout, {'next_page': '/'}),

                       url(r'^accounts/register', register),

                       url(r'^accounts/profile/', user_home),

                       url(r'^restaurants/', display_restaurants),

                       url(r'^vendor/menu/(?P<restaurant_id>\d+)', display_menu,name="view_menu"),

                       url(r'^food_order/add/(?P<food_item_id>\d+)', add_to_cart, name='item_added'),

                       url(r'^my_cart/(?P<menu_id>\d+)', get_food_cart),

                       url(r'^food_order/remove/(?P<food_item_id>\d+)', remove_from_cart, name='item_removed'),

                       #url(r'^get_stripe_user/',charge_customer),

                       url(r'^charge_customer/(?P<menu_id>\d+)',charge_customer),

                       # Stripe Payment URLS
                        url(r'^payments/',include("payments.urls")),

                       # Social auth for google login
                       url('', include('social.apps.django_app.urls', namespace='social')),

                       #url(r'/google_login/$',RedirectView.as_view(pattern_name='socialauth_begin')),
                       #url(r'^/complete/google-oauth2/', google_logi)




)
