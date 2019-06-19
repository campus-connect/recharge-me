#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings

class CustomUser(AbstractUser):
    
    GENDERCHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)
    gender = models.CharField(max_length=50, choices=GENDERCHOICES)
    date_of_birth = models.DateField("date of birth", blank=True, null=True)
    phone_number = models.CharField("phone number", max_length=20, null=True, blank=True)
    following = models.ManyToManyField("self", through='Peer', symmetrical=False, related_name='followers')

    def get_absolute_url(self):
        return reverse("user_account")

    
class Peer(models.Model):
    
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '%(user_from)s ---->> %(user_to)s' % {'user_from':self.user_from, 'user_to':self.user_to}