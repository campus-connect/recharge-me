#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django import template
from accounts.models import Peer, CustomUser

register = template.Library()


@register.simple_tag(takes_context=True)
def timer(context, user_from=None, user_to=None):

    request = context.get('request', None)
    if request:
        user = request.user
        if user.is_authenticated:
            if (user.task == CustomUser.USER_TASK_RECEIVE_FUNDING) & (user_from is not None):
                _time = Peer.objects.filter(user_from=user_from).filter(
                    user_to=user).get().expires_at
            elif (user.task == CustomUser.USER_TASK_SEND_FUNDING) & (user_to is not None):
                _time = Peer.objects.filter(user_to=user_to).filter(
                    user_from=user).get().expires_at
            else:
                _time = "dec 31, 2019 15:37:25"
        return _time
