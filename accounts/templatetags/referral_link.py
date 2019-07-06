#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import template
from django.urls import reverse
from django.core.cache import cache
from referrals.models import Link
from allauth.account.models import EmailAddress

register = template.Library()


@register.simple_tag(takes_context=True)
def referral_link(context):

    request = context.get('request', None)
    if request:
        address = request.build_absolute_uri(reverse('account_signup'))
        if request.user.is_authenticated:
            if EmailAddress.objects.filter(user=request.user, verified=True).exists():
                user = context['request'].user

                # Reduce database hits
                if '{}_referral_link'.format(user) in cache:
                    token = cache.get('{}_referral_link'.format(user))
                else:
                    try:
                        link = Link.objects.get(user=user)
                        token = link.token
                        cache.set(
                            '{}_referral_link'.format(user),
                            '{}'.format(token),
                            60*60*24
                        )
                    except Link.DoesNotExist:
                        return 'Token not found'

                    return '{}?&ref={}'.format(address, token)

            else:
                return 'Please verify your E-mail'
