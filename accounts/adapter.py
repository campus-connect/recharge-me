#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

import requests
from requests.exceptions import HTTPError
from django.conf import settings
from django.core.validators import validate_email
from django.forms import ValidationError
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        path = "/accounts/@{username}"
        return path.format(username=request.user.username)

    def clean_email(self, email):
        # validate email using built in logic
        validate_email(email)
        try:
            # validate domain
            email_domail = email.split('@')[1]
            res = requests.get('https://open.kickbox.com/v1/disposable/{}'.format(email_domail))
            is_disposable = res.json().get('disposable')
            if is_disposable:
                raise ValidationError('You are restricted from registering with disposable email.')
        except HTTPError:
            raise ValidationError('An error occurred while trying to valid your email. Please try again, if problem persist contact admin.')
        return email
