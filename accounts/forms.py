#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, AddEmailForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUserCreationForm will be used from django admin site
    and is only available to staff users during user creation
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    """
    CustomUserChangeForm will be used from django admin site
    and is only available to staff users during user update
    """
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomSignupForm(SignupForm):

    phone_number = PhoneNumberField()

    def save(self, request):
        """
        Adds extra field data to the user instance
        returns User object.
        """
        user = super(CustomSignupForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user

