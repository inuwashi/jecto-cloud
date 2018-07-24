from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from django.db.models import ExpressionWrapper, Value, DateField, F
from django.conf import settings


from .models import InjectionSite, Injection

import datetime
import logging
logger = logging.getLogger("django")


class InjectionSiteResource(DjangoResource):
    """Injection Site API Resource
    
    We are relying on restless http://restless.readthedocs.io 
    to generate the all the list end points with the added  
    last injection date in that for the logged in user.
    """

    preparer = FieldsPreparer(fields={
        'name': 'name',
        'pos_x': 'pos_x',
        'pos_y': 'pos_y',
        'last_injection' : 'last_injection'
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated
    
    def get_latest_injection_date(self,site):
        try:
            return Injection.objects.filter(
                site = site,
                user = self.request.user
                )[0].date
        except IndexError:
            return None

    # GET /api/sites/
    def list(self):

        logger.info("InjectionSite List API {} request to url {} with {} from {}".format(
            self.request.method,
            self.request.path,
            self.request.POST,
            self.request.META["REMOTE_ADDR"]
        ))
        injection_sites = InjectionSite.objects.all()
        for site in injection_sites:
            site.last_injection = self.get_latest_injection_date(site)
        return injection_sites




class InjectionResource(DjangoResource):
    """Injection API Resource
    
    We are relying on restless http://restless.readthedocs.io 
    to generate the all the list, details, and create end points.
    """

    preparer = FieldsPreparer(fields={
        'id' : 'id',
        'date' : 'date',
        'site' : 'site.name'
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated
        
    def wrap_list_response(self, data):
        """Refactoring to match bootgrid output"""
        return {
            "rows": data,
            "rowCount": 10,
            "total": len(data),
            "num_page": 1,
            "current": 1,
        }


    # GET /api/injections
    def list(self):
        logger.info("Injection List API {} request to url {} with {} from {}".format(
            self.request.method,
            self.request.path,
            self.request.POST,
            self.request.META["REMOTE_ADDR"]
        ))
        return Injection.objects.filter(user=self.request.user)[:10]

    # POST
    def create(self):
        logger.info("Injection Create API {} request to url {} with {} from {}".format(
            self.request.method,
            self.request.path,
            self.request.POST,
            self.request.META["REMOTE_ADDR"]
        ))
        return Injection.objects.create(
            site = InjectionSite.objects.get(name = self.data['site']),
            user = self.request.user,
            date = datetime.datetime.strptime(self.data['date'], "%Y-%m-%d").date()
        )
        