from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import  RequestContext
import json
from django.shortcuts import get_object_or_404, render_to_response, redirect
from forms import *
from meHungry_customer_website.models import *
from payments.models import *
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from carton.cart import *
import logging
import datetime, time
import os


cwd = os.getcwd()
#base = cwd[0:cwd.rindex('/')]
import sys


# Create your views here.

def homepage_view(request):
    return render_to_response('home.html',
                              {'title': "meHungry",
                               'body': "A startup project to revolutionize how you eat",
                               },
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html',context_instance=RequestContext(request))


def register(request):
    context = {}
    title = "Project X | Register "
    form = UserForm()
    created = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = MyUser(first_name=cd['first_name'],
                              last_name=cd['last_name'],
                              email=cd['email'],
                              )
            group = Group.objects.get(name="Customer")
            new_user.set_password(cd["password"])
            new_user.save()
            group.user_set.add(new_user) # Setting newly registered user in the Customer Group

            new_user = authenticate(email=request.POST['email'],
                                    password=request.POST['password'])
            stripe_user= Customer.create(new_user)
            CustomerProfile(user=new_user,payment_info=stripe_user).save()
            login(request, new_user)
            return redirect(user_home)
    context.update({'title': title, 'form': form, })
    return render_to_response('registration/register.html', context,context_instance=RequestContext(request))


def google_login(request):
    redirect(user_home)


@login_required
def user_home(request):
    context = {}
    context.update(csrf(request))
    title = "User"
    form = UpdateUserForm()
    success = None
    if request.method == 'POST':
        success = False
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            success = True
    context.update({'title':title,'form': form,'user':request.user,'success':success})
    return render_to_response('meHungry_customer_website/user_home.html',context)

def display_restaurants(request):
    context = {}
    title = "Restaurants"
    restaurant_list = Restaurant.objects.all()
    context.update({'title': title, 'restaurants': restaurant_list,'user':request.user})

    return render_to_response("meHungry_customer_website/restaurants.html", context,context_instance=RequestContext(request))


def display_menu(request, restaurant_id):

    context = {}
    title = "Menu"
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menuid = restaurant.menu.id
    menu = FoodItem.objects.filter(menu=menuid)
    context.update({'title': title, 'menu': menu, 'restaurant': restaurant, 'user': request.user, 'menuid': menuid})
    return render_to_response("meHungry_customer_website/vendor/menu.html", context, context_instance=RequestContext(request))


@login_required
def add_to_cart(request, food_item_id):

    context ={}
    context.update(csrf(request))
    food_item = get_object_or_404(FoodItem , pk=food_item_id)
    food_cart = Cart(session=request.session, session_key=('CART-'+str(food_item.menu.id)))
    food_cart.add(food_item, price=food_item.price)
    # save cart into session
    request.session['CART-'+str(food_item.menu.id)] = food_cart.cart_serializable
    context={'user': request.user.serializable_value(field_name="first_name"), 'menuid': food_item.menu.id}
    return HttpResponse(json.dumps(context),content_type="application/json")

@login_required
def remove_from_cart(request, food_item_id):

    context = {}
    context.update(csrf(request))
    context.update({'user':request.user})
    food_item = get_object_or_404(FoodItem , pk=food_item_id)
    food_cart = Cart(session=request.session, session_key=('CART-'+str(food_item.menu.id)))
    # save cart into session
    request.session['CART-'+str(food_item.menu.id)] = food_cart.cart_serializable
    food_cart.remove_single(food_item)



    return HttpResponse("Removed")



@login_required
def get_food_cart(request, menu_id):

    context = {}
    context.update(csrf(request))
    customer_profile=CustomerProfile.objects.get(user=request.user) # Need to put a try catch block for customers without a customer profile.
    food_cart = Cart(session=request.session, session_key=('CART-'+str(menu_id)))
    grand_total = food_cart.total
    dollar_total=int (food_cart.total * Decimal(100))
    context.update({'user':request.user, 'food_cart': food_cart, 'customer_profile':customer_profile,'grand_total':grand_total, 'dollar_total':dollar_total,'menuid':menu_id })
    return render_to_response('meHungry_customer_website/show-cart.html',context )

# Charge customer method for django-stripe-payments method
@login_required
def charge_customer(request,menu_id):

    context={}

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account
    stripe.api_key = "sk_test_QOyWGJcHtngXcQNyyu5y8o52"


    # Getting total price from the cart in the session
    food_cart = Cart(session=request.session, session_key=('CART-'+str(menu_id)))
    total_amount =food_cart.total

    # Getting the order restaurant
    #restaurant= Restaurant.get(pk=restaurant_id)



    # Checking if user exists in Payments Database Customer Table
    try:

        # Important Note: stripe_user gets object from Customer table from OUR Payments Database
        # stripe_customer is an attribute of stripe_user which resides on the Stripe Database on Stripe servers.
        stripe_user=Customer.objects.get(user=request.user)

    except:

        # Creating a new user on Payments Database and also on Stripe Database on Stripe server
        stripe_user= Customer.create(request.user)



    #########################   I M P O R T A N T ################################ I M P O R T A N T ################################# I M P O R T A N T ########################################

    # IMPORTANT !!!!!!!!!!      Error in django-stripe-package  virtual_env/lib/python2.7/site-packages/payments/models.py  LINE 594 change "captured=capture" to "capture=capture"
    # Changes also made to INSTALLED_APPS in settings.py. Added a 'django.contrib.sites' app. Run python manage.py migrate to update database before running the server again.
    # Detailed Error and Bug log pending

    #########################   I M P O R T A N T ################################ I M P O R T A N T ################################# I M P O R T A N T ########################################

    if stripe_user.stripe_customer.active_card: # checks if customer has card info on the Payments database

        # Charging customer with the card saved on the database
        stripe_user.charge(total_amount)

        new_food_order=FoodOrder(customer=request.user,
                                 #restaurant= restaurant,
                                 order_price= total_amount)
        new_food_order.save()

        for item in food_cart.products:
            new_food_order.orderItems.add(item)
        #FoodOrder.customer=
        return HttpResponse("Card Accepted")

    else:

        # Getting the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Getting the users email address
        #user_email =  request.POST['stripeEmail']

        # Getting token information from the newly created token and updating the Customer table in Payments Database
        stripe_user.update_card(token)

        #Saving all updates
        stripe_user.save_card(stripe_user.stripe_customer)

        # Charging Customer for the
        stripe_user.charge(food_cart.total)
        new_food_order=FoodOrder(customer=request.user,
                                 #restaurant= restaurant,
                                 order_price= total_amount)
        new_food_order.save()

        for item in food_cart.products:
            new_food_order.orderItems.add(item)

        return HttpResponse("Card Info saved and Card Accepted")

   #To be used when post-checkout pages are designed
    #context.update({'stripe_user':stripe_user, 'message':message})

   # return  render_to_response('meHungry_customer_website/show-cart.html',context)




