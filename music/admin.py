from django.contrib import admin
from .models import Artist, ChartHistory, Genre, Album, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "artist",
        "release_date",
    )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "artist",
        "album",
        "genre",
        "plays",
        "downloads",
        "allow_download",
        "uploaded_at",
    )

    list_filter = (
        "genre",
        "artist",
        "album",
        "allow_download",
    )

    search_fields = (
        "title",
        "artist__name",
        "album__title",
    )


@admin.register(ChartHistory)
class ChartHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "chart_date",
        "rank",
        "song",
        "created_at",
    )

    list_filter = (
        "chart_date",
    )

    search_fields = (
        "song__title",
        "song__artist__name",
    )

    ordering = (
        "-chart_date",
        "rank",
    )