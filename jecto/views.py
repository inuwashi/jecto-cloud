from django.views import generic, View
from django.http import Http404
from django.shortcuts import render, redirect
from jecto.models import Injection, InjectionSite

import datetime




# Views 

class HomePage(View):

    def prep_sites(self, user):
        """Generated an updated site list for a user.
        
        Generate a list of all available Injection Sites and add to each:
            1. The  last injection date in that site for the user.
            2. The display color for the site marker.

        Attributes:
            user (authtools.user) : The user object to filter by.

        Returns;
            A QuerySet of InjectionSites objects over loaded with the most 
            recent injection date for that suer and a calculated RRGGBB color code. 

            Color Calculation is done to indicate to the user which injection sites
            are the safest by setting the RRGGB code of the site indicator. By setting 
            the Green value to the diff between the last injection date and today in days
            and setting the Red value to be 10 (*) minus eh green value we et a nice gradient 
            from Green to Red with the Blue adding a nice tint. 
            * All injection sites that have not been used in 10 days are set to Green.
            ** Note that the number 10 was chosen becurse going all the way up to F resulted
            in an annoying fluorescent shades. 

        """

        injection_sites = InjectionSite.objects.all()
        today = datetime.date.today()
        for site in injection_sites:
            try:
                site.last_injection =  Injection.objects.filter(
                    site = site,
                    user = user
                    )[0].date
                age = (today - site.last_injection).days
                if age > 10:
                    site.color = '#009944'
                if age < 0:
                    site.color = '#990044'
                else:
                    red = 10-age
                    green = 10-red
                    site.color = '#{}{}44'.format(
                        str(red)*2,
                        str(green)*2
                    )
            except IndexError:
                site.last_injection  = datetime.date(1970,1,1)
                site.color = "#009944"

        return injection_sites

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(self.request,"splash.html")
        else:

            # Clean up injection dates 
            # Todo : Handle user time zone.
            last_injection = Injection.objects.filter(user = self.request.user).latest('date')
            next_injection_date  = last_injection.date+datetime.timedelta(days=self.request.user.profile.frequency)
            should_inject = next_injection_date <= datetime.date.today()

            # Prep Injection sites 
           

            return render(self.request,"home.html",{
                "last_injection" : last_injection,
                "next_injection_date" : next_injection_date,
                "should_inject" : should_inject,
                "sites" : self.prep_sites(self.request.user)
            })

class AboutPage(generic.TemplateView):
    template_name = "about.html"


