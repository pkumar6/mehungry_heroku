__author__ = 'pranaykumar'

from meHungry_customer_website.models import MyUser
from django.forms import ModelForm
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _


class MetaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MetaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(MetaForm):
    class Meta:  # virtual_env/lib/python2.7/site-packages/django/forms/forms.py
        password = forms.CharField(widget=forms.PasswordInput())
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            }

class UpdateUserForm(MetaForm):
    class Meta:
        # forms.py
        model = User
        fields = ['first_name', 'last_name']

class MyUserCreationForm(forms.ModelForm):

    """ A form for creating new users.
    Includes all the required fields, plus a repeated password.
    """

    error_messages = {
        'duplicate_email': _("A user with that email already exists.")
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_email(self):
        """ Clean form email.
        :return str email: cleaned email
        :raise forms.ValidationError: Email is duplicated
        """
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def save(self, commit=True):
        """ Save user.
        Save the provided password in hashed format.
        :return custom_user.models.EmailUser: user
        """
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):

    """ A form for updating users.
    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = MyUser
        exclude = ()

    def __init__(self, *args, **kwargs):
        """ Init the form."""
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """ Clean password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.
        :return str password:
        """
        return self.initial["password"]