#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.urls import path
from .views import (
    Dashboard,
    ProfileUpdateView
)

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("@<username>", ProfileUpdateView.as_view(), name="user_profile")
]