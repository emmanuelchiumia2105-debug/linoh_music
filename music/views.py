from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Song, ChartHistory


def home(request):
    trending_songs = Song.objects.order_by("-plays")[:4]

    latest_songs = Song.objects.order_by("-uploaded_at")[:6]

    chart_songs = list(
        Song.objects.order_by("-plays")[:10]
    )

    today = timezone.localdate()

    # Get the most recent chart before today
    previous_chart = {}

    previous_entries = (
        ChartHistory.objects
        .filter(chart_date__lt=today)
        .order_by("-chart_date", "rank")
    )

    # Keep only the latest rank for each song
    for entry in previous_entries:
        if entry.song_id not in previous_chart:
            previous_chart[entry.song_id] = entry.rank

    # Calculate movement
    for current_rank, song in enumerate(chart_songs, start=1):

        song.current_rank = current_rank

        previous_rank = previous_chart.get(song.id)

        if previous_rank is None:
            song.movement = 0
            song.movement_type = "new"

        elif previous_rank > current_rank:
            song.movement = previous_rank - current_rank
            song.movement_type = "up"

        elif previous_rank < current_rank:
            song.movement = current_rank - previous_rank
            song.movement_type = "down"

        else:
            song.movement = 0
            song.movement_type = "same"

    context = {
        "trending_songs": trending_songs,
        "latest_songs": latest_songs,
        "chart_songs": chart_songs,
    }

    return render(
        request,
        "music/home.html",
        context
    )

def record_play(request, song_id):

    song = get_object_or_404(Song, id=song_id)

    song.plays += 1

    song.save(update_fields=["plays"])

    return JsonResponse({
        "success": True,
        "plays": song.plays,
    })