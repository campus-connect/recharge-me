#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        path = "/accounts/@{username}"
        return path.format(username=request.user.username)