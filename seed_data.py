import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_discovery_project.settings")
import django
django.setup()

from movies.models import BookingHistory, Movie, RecentlyViewed, Theater

Theater.objects.all().delete()
Movie.objects.all().delete()
BookingHistory.objects.all().delete()
RecentlyViewed.objects.all().delete()

cineplex = Theater.objects.create(name="Cineplex", city="Mumbai")
inox = Theater.objects.create(name="INOX", city="Delhi")
pvr = Theater.objects.create(name="PVR", city="Bangalore")

movies = [
    {"title": "Inception", "genre": "Sci-Fi", "language": "English", "release_date": "2024-01-15", "rating": 8.8, "ticket_price": 12.50, "show_timings": ["19:30", "22:00"], "popularity": 35, "theater": cineplex},
    {"title": "Interstellar", "genre": "Sci-Fi", "language": "English", "release_date": "2024-01-20", "rating": 9.0, "ticket_price": 14.75, "show_timings": ["18:00", "21:00"], "popularity": 40, "theater": inox},
    {"title": "The Dark Knight", "genre": "Action", "language": "English", "release_date": "2024-02-01", "rating": 8.7, "ticket_price": 11.25, "show_timings": ["17:30", "20:15"], "popularity": 30, "theater": pvr},
    {"title": "RRR", "genre": "Action", "language": "Telugu", "release_date": "2024-02-10", "rating": 8.5, "ticket_price": 10.50, "show_timings": ["15:00", "19:00"], "popularity": 28, "theater": cineplex},
    {"title": "Parasite", "genre": "Thriller", "language": "Korean", "release_date": "2024-03-01", "rating": 8.9, "ticket_price": 13.25, "show_timings": ["20:00", "23:00"], "popularity": 33, "theater": inox},
    {"title": "Dangal", "genre": "Drama", "language": "Hindi", "release_date": "2024-03-15", "rating": 8.4, "ticket_price": 9.50, "show_timings": ["16:30", "19:45"], "popularity": 29, "theater": pvr},
]

for data in movies:
    movie = Movie.objects.create(**{k: v for k, v in data.items() if k != "theater"}, theater=data["theater"])
    if movie.title == "Inception":
        BookingHistory.objects.create(movie=movie, user_name="guest")
        RecentlyViewed.objects.create(movie=movie, user_name="guest")

print("Seeded movie discovery data")
