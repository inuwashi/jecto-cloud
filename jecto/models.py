from django.db import models
from django.conf import settings


class InjectionSite(models.Model):
    """Injection zones on the body

    We keep track of the available injection sites on the body, and how we
    display them. In the future we should allow users to create costume sites.
    """
    name = models.CharField(max_length=32, help_text='Zone name. E.g. Left Thigh.')
    pos_x = models.SmallIntegerField(help_text='Display X Position on the Vitruvian Man Image.')
    pos_y = models.SmallIntegerField(help_text='Display Y Position on the Vitruvian Man Image.')

    def __unicode__(self):
        return "[Zone:{}]".format(self.name)

class Injection(models.Model):
    """An Injection record made by a user in an Injection Zone.

    Attributes: 
        Injection records are a simple collection of:
        date (date) : Date fo injection.
        zone (key : zone) : The zone used for eh injection.
        
    """
    date = models.DateField('Injection Date', auto_now_add=True)
    site = models.ForeignKey(InjectionSite, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    def __unicode__(self):
        return "[Injection:{} {} on {}]".format(
                        self.user.email,
                        self.zone.name, 
                        self.date
                        )