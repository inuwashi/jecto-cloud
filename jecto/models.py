from django.db import models
from django.conf import settings
import datetime

class InjectionSite(models.Model):
    """Injection sites on the body

    We keep track of the available injection sites on the body, and how we
    display them. In the future we should allow users to create costume sites.

    Attributes:
        name (str) : Site name. E.g. Left Thigh.
        pos_x (int) : Display X Position on the Vitruvian Man Image.
        pos_y (int) : Display Y Position on the Vitruvian Man Image.
    """
    name = models.CharField(max_length=32)
    pos_x = models.SmallIntegerField()
    pos_y = models.SmallIntegerField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Injection Sites"

    def __str__(self):
        return "[Injection Site : {}]".format(self.name)

class Injection(models.Model):
    """An Injection record made by a user in an Injection Site.

    Attributes: 
        Injection records are a simple collection of:
        date (date) : Date fo injection.
        site (key : site) : The site used for the injection.
    """
    date = models.DateField('Injection Date', default = datetime.date.today)
    site = models.ForeignKey(InjectionSite, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Injections"
    
    def __str__(self):
        return "[Injection : {} {} on {}]".format(
                        self.user.email,
                        self.site.name, 
                        self.date
                        )