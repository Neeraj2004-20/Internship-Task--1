from django.db import models


class Theater(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.FloatField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    show_timings = models.JSONField(default=list, blank=True)
    popularity = models.PositiveIntegerField(default=0)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name="movies")

    class Meta:
        ordering = ["-popularity"]

    def __str__(self):
        return self.title


class BookingHistory(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    user_name = models.CharField(max_length=100, default="guest")

    def __str__(self):
        return f"{self.user_name} -> {self.movie.title}"


class RecentlyViewed(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="views")
    user_name = models.CharField(max_length=100, default="guest")

    def __str__(self):
        return f"{self.user_name} -> {self.movie.title}"
