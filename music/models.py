from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="artists/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums"
    )

    cover = models.ImageField(
        upload_to="albums/",
        blank=True,
        null=True
    )

    release_date = models.DateField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="songs"
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="songs"
    )

    audio_file = models.FileField(
        upload_to="songs/"
    )

    cover = models.ImageField(
        upload_to="song_covers/",
        blank=True,
        null=True
    )

    plays = models.PositiveIntegerField(default=0)

    downloads = models.PositiveIntegerField(default=0)

    allow_download = models.BooleanField(default=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChartHistory(models.Model):
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="chart_history"
    )

    rank = models.PositiveIntegerField()

    chart_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["rank"]
        unique_together = ("song", "chart_date")

    def __str__(self):
        return f"{self.chart_date} - #{self.rank} - {self.song.title}"
    
