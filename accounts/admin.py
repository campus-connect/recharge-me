#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Peer


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'phone_number']
    # list_editable = ['phone_number']
    list_filter = ['date_joined', 'last_login', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'phone_number']
    
    model = CustomUser


@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):

    list_display = ['user_from', 'user_to', 'created_at', 'expires_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = [
        'user_from__username', 'user_from__firstname', 'user_from__lastname',
        'user_to__username', 'user_to__firstname', 'user_to__lastname'
    ]