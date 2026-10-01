from django.core.management.base import BaseCommand
from django.utils import timezone

from music.models import Song, ChartHistory


class Command(BaseCommand):
    help = "Save today's top 10 songs to chart history."

    def handle(self, *args, **options):

        today = timezone.localdate()

        # Prevent creating the same chart twice
        if ChartHistory.objects.filter(chart_date=today).exists():

            self.stdout.write(
                self.style.WARNING(
                    f"Chart for {today} already exists."
                )
            )

            return

        songs = Song.objects.order_by("-plays")[:10]

        if not songs:

            self.stdout.write(
                self.style.WARNING(
                    "No songs available for the chart."
                )
            )

            return

        chart_entries = []

        for rank, song in enumerate(songs, start=1):

            chart_entries.append(
                ChartHistory(
                    song=song,
                    rank=rank,
                    chart_date=today,
                )
            )

        ChartHistory.objects.bulk_create(chart_entries)

        self.stdout.write(
            self.style.SUCCESS(
                f"Chart updated successfully for {today}."
            )
        )