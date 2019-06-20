#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    
    USER_TASK_SEND_FUNDING = 'S'
    USER_TASK_RECEIVE_FUNDING = 'R'
    USER_TASK_DEFAULT = USER_TASK_SEND_FUNDING
    USER_TASK_CHOICES = (
        (USER_TASK_SEND_FUNDING, 'Send funding'), # send funding
        (USER_TASK_RECEIVE_FUNDING, 'Receive funding') # receive funding
    )
    GENDERCHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )


    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)
    gender = models.CharField(max_length=2, choices=GENDERCHOICES)
    date_of_birth = models.DateField("date of birth", blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name = "phone number", null=True, blank=True)
    following = models.ManyToManyField("self", through='Peer', symmetrical=False, related_name='followers')
    level = models.ForeignKey("Level", on_delete=models.SET_NULL, null=True)
    task = models.CharField(max_length=2, choices=USER_TASK_CHOICES, default=USER_TASK_DEFAULT)
    amount_sent = models.DecimalField("Amount sent", max_digits=8, decimal_places=2, default=0)
    amount_received = models.DecimalField("Amount received", max_digits=8, decimal_places=2, default=0)
    karma = models.FloatField(default=10)

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

class Level(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    entry_fee = models.DecimalField("Entry fee", max_digits=8, decimal_places=2, help_text="Amount user must send to eligible user")
    level_reward = models.DecimalField("Level reward", max_digits=8, decimal_places=2, help_text="Amount users will receive")

    class Meta:
        verbose_name = "level"
        verbose_name_plural = "levels"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("level_detail", kwargs={"pk": self.pk})
