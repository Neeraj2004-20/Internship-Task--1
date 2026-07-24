from django.contrib import admin
from .models import BookingHistory, Movie, RecentlyViewed, Theater

admin.site.register(Theater)
admin.site.register(Movie)
admin.site.register(BookingHistory)
admin.site.register(RecentlyViewed)
