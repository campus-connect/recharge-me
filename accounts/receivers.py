#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

import logging
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up, email_confirmed, email_changed
from referrals.signals import create_flat_referral
from referrals.models import Link

logger = logging.getLogger(__name__)

@receiver(user_signed_up)
def create_referral(sender, **kwargs):
    """
    This function is more of a middleman, it signals the referral to
    validate and create referral
    """

    create_flat_referral.send(sender=get_user_model(), request=kwargs['request'], user=kwargs['user'])


@receiver(email_confirmed)
def create_referral_token(sender, **kwargs):
    """
    creates a referral token, only after email has been confirm
    """
    Link.objects.create(user=kwargs['user'])


@receiver(email_changed)
def delete_referral_token(sender, **kwargs):
    """
    Only user with verified email can have referral token
    """
    try:
        link = Link.objects.get(user=kwargs['user'])
        link.delete() 
        # TODO: send an email/onsite notification to user
    except Link.DoesNotExist:
        logger.exception('No token found for user with username {} '.format(kwargs['user'].username))