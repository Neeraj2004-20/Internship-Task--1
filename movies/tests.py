from django.test import TestCase
from django.urls import reverse

from .models import BookingHistory, Movie, RecentlyViewed, Theater


class MovieDiscoveryTests(TestCase):
    def setUp(self):
        theater = Theater.objects.create(name="Cineplex", city="Mumbai")
        self.movie = Movie.objects.create(
            title="Inception",
            genre="Sci-Fi",
            language="English",
            release_date="2024-01-15",
            rating=8.8,
            ticket_price=12.50,
            show_timings=["19:30", "22:00"],
            popularity=35,
            theater=theater,
        )
        BookingHistory.objects.create(movie=self.movie, user_name="guest")
        RecentlyViewed.objects.create(movie=self.movie, user_name="guest")

    def test_discovery_page_renders_and_filters(self):
        response = self.client.get(reverse("movie-discovery"), {"genre": "Sci-Fi", "sort_by": "rating"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "Recommended for You")
