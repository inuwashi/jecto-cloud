from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings


class BaseProfile(models.Model):
    """Expending the Django user objects:

        Attributes:
            user (OneToOne) : The user we are expending.
            slug (uuid4) : UUID for obj reference  (came with edge) in URL.
            picture (file): A user thumbnail (came with edge).
            bio (char) : Short description of the user (came with edge).
            email_verified (bool) : Email verification check  (came with edge).
            frequency (int): How often is this user supppsoed to injecting 
                their medication, represented by number of days between
                injections. 

    """
    DAILY = 1
    BIDAILY = 2
    WEEKLY = 7
    MONTHLY = 30
    FREQUENCY_CHOICES = (
        (DAILY, 'Every Day'),
        (BIDAILY, 'Every Other Day'),
        (WEEKLY, 'Every Week'),
        (MONTHLY, 'Every Monthly'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)
    frequency = models.IntegerField(
        choices=FREQUENCY_CHOICES,
        default=DAILY,
    )


    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{}'s profile". format(self.user)
