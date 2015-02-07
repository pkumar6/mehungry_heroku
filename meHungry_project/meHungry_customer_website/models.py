from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.sites.models import Site
from payments.models import Charge, Customer
from jsonfield import JSONField
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, is_admin, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_admin, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=True, is_active=True,
                          is_superuser=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyAbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('admin status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class MyUser(MyAbstractUser):

    """
    Concrete class of AbstractEmailUser.
    Use this if you don't need to extend EmailUser.
    """

    class Meta(MyAbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, limit_choices_to={'groups': "2"}, null=True, related_name='user')
    payment_info = models.OneToOneField(Customer, null=True)

    def __unicode__(self):
        return self.user.email


class Address(models.Model):
    customer_profile = models.ForeignKey(CustomerProfile)
    street = models.CharField(max_length=50, null=True)
    apt = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    zip = models.IntegerField(max_length=5, null=True)


class Bar(models.Model):
    barName = models.CharField(max_length=50)
    vendor = models.OneToOneField(settings.AUTH_USER_MODEL, limit_choices_to={'groups': "1"})
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50)
    # To be changed to a drop down menu of preloaded states and cities
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    foodMenu = models.BooleanField(default=False)
    # menu         = models.ForeignKey(Menu)
    barType = models.CharField(max_length=20)

    def __unicode__(self):
        return self.barName


class Menu(models.Model):
    menuName = models.CharField(max_length=50, null=True)
    # foodItems = models.ManyToManyField(FoodItem,null=True)

    def __unicode__(self):
        return self.menuName


class FoodItem(models.Model):
    itemName = models.CharField(max_length=30, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    menu = models.ForeignKey(Menu, null=True)
    # TODO: description of food

    def __unicode__(self):
        return self.itemName


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=15)
    menu = models.OneToOneField(Menu, null=True)
    # TODO: restaurants logo/chef photo url or save on our server
    desc = models.TextField(max_length=250)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=10)
    # tags to be implemented for the search engine
    # tags  =
    delivery = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def getFood(self):
        return FoodItem.objects.filter(menu = self.menu)


class Package(models.Model):
    bar = models.ForeignKey(Bar)
    packageName = models.CharField(max_length=50)
    packageCost = models.DecimalField(max_digits=6, decimal_places=2)
    # packageService Attribute will be used to list the services of the package
    # packageService =

    def __unicode__(self):
        return self.packageName


class Event(models.Model):
    eventName = models.CharField(max_length=250)
    eventType = models.CharField(max_length=50)
    eventDate = models.DateField()
    eventTime = models.TimeField()
    budget = models.DecimalField(max_digits=6, decimal_places=2)
    totalCost = models.DecimalField(max_digits=6, decimal_places=2)

    # For future implementation of private/reverse bidding
    # offeredCost= models.DecimalField(max_digits=6,decimal_places=2)

    # Foreign Keys
    customer = models.ForeignKey(MyUser)
    bar = models.ForeignKey(Bar)
    package = models.ForeignKey(Package)

    def __unicode__(self):
        return self.eventName


class FoodOrder(models.Model):


    restaurant = models.ForeignKey(Restaurant,null=True)

    # "groups" is the group.id from the auth_group table
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'groups': "2"}, null=True)
    orderItems = models.ManyToManyField(FoodItem, null=True)
    # vendorInfo = models.ForeignKey(User, related_name='is_staff'
    # Price of the order according to the Menu
    #menuPrice = models.DecimalField(max_digits=6, decimal_places=2)

    charge_info = models.OneToOneField(Charge,null=True)
    order_price = models.DecimalField(max_digits=6,decimal_places=2,null=True)

    # Price offered by the customer for the food order
    # bidPrice = models.DecimalField(max_digits=6, decimal_places=2)
    # foodItems attribute will contain the customer's order in xml formant
    # foodItems =

    address_info = models.ForeignKey(Address, null=True)

    delivery = models.BooleanField(default=False)

    # paymentMethod to be activated while implementing the transaction engine
    # paymentMethod  =
    # To check the status of the order option set to be implemented
    # orderStatus
    # vendorApproval to be determined after the order is viewed by the vendor
    # vendorApproval =  option set to be implemented

    def __unicode__(self):
        return self.customer.username


class Deliveries(models.Model):
    deliveryPerson = models.OneToOneField(settings.AUTH_USER_MODEL, limit_choices_to={'groups': "3"}, null=True)
    foodOrderInfo = models.ForeignKey(FoodOrder)
    deliveryCompleted = models.BooleanField(default=False)
    '''deliveryApt = models.ForeignKey(FoodOrder.deliveryApt)
    deliveryCity = models.ForeignKey(FoodOrder.deliveryCity)
    deliveryState = models.ForeignKey(FoodOrder.deliveryState)
    deliveryZip = models.ForeignKey(FoodOrder.deliveryZip)'''

    def __unicode__(self):
        return self.deliveryPerson.username


class PickUps(models.Model):
    pickUpPerson = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'groups': "3"}, null=True)
    pickUpRestaurant = models.ForeignKey(FoodOrder, null=True)