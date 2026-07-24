from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import BookingHistory, Movie, RecentlyViewed, Theater


def _get_recommendations(user_name: str):
    history_ids = list(BookingHistory.objects.filter(user_name=user_name).values_list("movie_id", flat=True))
    viewed_ids = list(RecentlyViewed.objects.filter(user_name=user_name).values_list("movie_id", flat=True))
    related_ids = history_ids + viewed_ids

    if not related_ids:
        return Movie.objects.none()

    return (
        Movie.objects.filter(id__in=related_ids)
        .order_by("-popularity")[:4]
    )


def movie_discovery_view(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    language = request.GET.get("language", "")
    city = request.GET.get("city", "")
    theater = request.GET.get("theater", "")
    release_date = request.GET.get("release_date", "")
    rating = request.GET.get("rating", "")
    show_time = request.GET.get("show_time", "")
    sort_by = request.GET.get("sort_by", "popularity")
    page_number = request.GET.get("page", 1)

    queryset = Movie.objects.select_related("theater")

    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(genre__icontains=query))
    if genre:
        queryset = queryset.filter(genre__iexact=genre)
    if language:
        queryset = queryset.filter(language__iexact=language)
    if city:
        queryset = queryset.filter(theater__city__iexact=city)
    if theater:
        queryset = queryset.filter(theater__name__iexact=theater)
    if release_date:
        queryset = queryset.filter(release_date=release_date)
    if rating:
        queryset = queryset.filter(rating__gte=float(rating))
    if show_time:
        queryset = queryset.filter(show_timings__contains=[show_time])

    order_map = {
        "popularity": "-popularity",
        "newest": "-release_date",
        "rating": "-rating",
        "price": "ticket_price",
    }
    queryset = queryset.order_by(order_map.get(sort_by, "-popularity"))

    paginator = Paginator(queryset, 6)
    page_obj = paginator.get_page(page_number)

    context = {
        "movies": page_obj,
        "recommendations": _get_recommendations("guest"),
        "genres": Movie.objects.values_list("genre", flat=True).distinct().order_by("genre"),
        "languages": Movie.objects.values_list("language", flat=True).distinct().order_by("language"),
        "cities": Theater.objects.values_list("city", flat=True).distinct().order_by("city"),
        "theaters": Theater.objects.values_list("name", flat=True).distinct().order_by("name"),
        "selected": {
            "q": query,
            "genre": genre,
            "language": language,
            "city": city,
            "theater": theater,
            "release_date": release_date,
            "rating": rating,
            "show_time": show_time,
            "sort_by": sort_by,
        },
        "total_count": queryset.count(),
    }
    return render(request, "movies/discovery.html", context)
