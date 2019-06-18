#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    
    GENDERCHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)
    gender = models.CharField(max_length=50, choices=GENDERCHOICES)
    date_of_birth = models.DateField("date of birth", blank=True, null=True)
    phone_number = models.CharField("phone number", max_length=20, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("user_account")