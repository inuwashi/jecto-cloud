from django.contrib import admin
from .models import InjectionSite,Injection


@admin.register(InjectionSite)
class InjectionSiteAdmin(admin.ModelAdmin):
    fields = ('name', 'pos_x', 'pos_y')
    list_display = ('name', 'position')

    def position(self, obj):
        return "{}x{}".format(obj.pos_x,obj.pos_y)


@admin.register(Injection)
class InjectionAdmin(admin.ModelAdmin):
    fields = ('user', 'site', 'date')
    list_display = ('user', 'site', 'date')
    list_filter = ('site', 'user')
    search_fields = ['user__email', 'date']


