from django.views import generic, View
from django.http import Http404
from django.shortcuts import render, redirect

# Helpers

def parseDate(year, month, day):
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        return Date(year, month, day)
    except (ValueError, TypeError) as t:
        raise ValueError(t)

def injectionHistory(startDay, numDays=30):
    earliestDay = startDay + TimeDelta(days = -numDays)
    relevantInjections = Injection.objects.filter(date__lte = startDay).filter(date__gt = earliestDay)
    return relevantInjections.order_by("date").reverse()  # Newest to oldest

def datesToColors(dates):
    """
    Returns a list of (Date, color) ordered by Date.
    """
    allDates = dates
    dates = [date for date in allDates if date is not None]
    addNones = [(None, "#CCF")] * (len(allDates) - len(dates))
    dates.sort()
    if not dates: return addNones
    if len(dates) == 1: return addNones + [(dates[0], "#F00")]
    lowest = dates[0]
    highest = dates[-1]
    dateRange = float((highest - lowest).days)
    res = []
    for day in dates:
        unTensity = int(255.0 * (highest - day).days / dateRange)
        color = "#FF%s" % (hex(unTensity)[-2:] * 2)
        res.append((day, color))
    return addNones + res


# Views 

class HomePage(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(self.request,"splash.html")
        else:
            return render(self.request,"home.html")

class AboutPage(generic.TemplateView):
    template_name = "about.html"


