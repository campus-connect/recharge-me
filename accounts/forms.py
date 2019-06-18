#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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