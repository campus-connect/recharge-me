#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, AddEmailForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from referrals.widgets import ReferralWidget
from referrals.fields import ReferralField
from .models import CustomUser, Level, Peer
from . import verbs


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
    referral = ReferralField(widget=ReferralWidget())

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail address',
                'autofocus': 'autofocus'
            }
        )

        self.fields['phone_number'].widget = PhoneNumberInternationalFallbackWidget(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password (again)'
            }
        )

    def save(self, request):
        """
        Adds extra field data to the user instance
        returns User object.
        """
        user = super(CustomSignupForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username or e-mail',
                'autofocus': 'autofocus'
            }
        )

        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )

        self.fields['remember'].widget = forms.CheckboxInput(
            attrs={
                'class': 'custom-control-input'
            }
        )


class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail address'
            }
        )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number',
                  'date_of_birth', )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofill': False
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofill': False
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofill': False
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'autofill': False
                }
            )
        }


class LevelEnrollmentForm(forms.Form):

    action = forms.CharField()

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request', None)

        super(LevelEnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['action'].widget = forms.HiddenInput(
            attrs={
                'value': self.get_action()
            }
        )

    def get_action(self):
        if self.request.user.level is not None:
            return 'un_enroll'
        else:
            return 'enroll'

    def get_entry_level(self):
        """
        Entry Level should have an order of 1
        """
        try:
            entry_level = Level.objects.get(order=1)
            return entry_level
        except Level.DoesNotExist:
            return None

    def get_next_level(self):
        user_current_level = self.request.user.level
        if user_current_level:
            try:
                next_level = Level.objects.get(
                    order=user_current_level.order+1)
                return next_level
            except Level.DoesNotExist:
                return self.get_entry_level()
        else:
            return self.get_entry_level()

    def enroll(self):
        try:
            user = CustomUser.objects.get(pk=self.request.user.id)
            user.level = self.get_entry_level()
            user.can_merge = True
            user.save()
            messages.success(self.request, verbs.ENROL)
        except CustomUser.DoesNotExist:
            pass

    def un_enroll(self):
        if (Peer.objects.filter(Q(user_from=self.request.user) | Q(user_to=self.request.user)).count() == 0) and (self.request.user.task == CustomUser.USER_TASK_SEND_FUNDING):
            try:
                user = CustomUser.objects.get(pk=self.request.user.id)
                user.level = None
                user.can_merge = False
                user.save()
                messages.success(self.request, verbs.UN_ENROL)
            except CustomUser.DoesNotExist:
                pass
        else:
            if self.request.user.task == CustomUser.USER_TASK_RECEIVE_FUNDING:
                messages.error(self.request, verbs.UN_ENROL_ERROR_DISALLOW)
            else:
                messages.error(self.request, verbs.UN_ENROL_ERROR)


class ConfirmationForm(forms.Form):

    action = forms.CharField(required=True, widget=forms.HiddenInput)
    target = forms.IntegerField(required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request', None)
        super(ConfirmationForm, self).__init__(*args, **kwargs)

        peers = self.get_peers(self.request)
        for i in range(len(peers)):
            field_name = 'user_%s' % (i,)
            self.fields[field_name] = forms.CharField(
                required=False,
                widget=forms.HiddenInput
            )
            try:
                self.initial[field_name] = peers[i].id
            except IndexError:
                self.initial[field_name] = ""

    def get_peers(self, request):
        user = self.request.user
        if user.task == CustomUser.USER_TASK_RECEIVE_FUNDING:
            return user.followers.all()
        elif user.task == CustomUser.USER_TASK_SEND_FUNDING:
            return user.following.all()

    def get_user_from_field(self):
        for field_name in self.fields:
            if field_name.startswith('user_'):
                yield self[field_name]

    # def clean(self):
    #     users = set()
    #     i = 0
    #     field_name = 'user_%s' % (i,)
    #     while self.cleaned_data.get(field_name):
    #        user = self.cleaned_data[field_name]
    #        if user in users:
    #            self.add_error(field_name, 'Duplicate')
    #        else:
    #            users.add(user)
    #        i += 1
    #        field_name = 'user_%s' % (i,)
    #     self.cleaned_data['users'] = users
