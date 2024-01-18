from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    DirectorsViewSet,
    StudiosViewSet,
    MoviesViewSet,
    MediaFileViewSet,
    movie_recommendations,
)

router = DefaultRouter()
router.register(r"directors", DirectorsViewSet, basename="directors")
router.register(r"studios", StudiosViewSet, basename="studios")
router.register(r"movies", MoviesViewSet, basename="movies")
router.register(r"media-files", MediaFileViewSet, basename="media-files")

urlpatterns = [
    path(
        "directors/<int:id>/",
        DirectorsViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="director-detail",
    ),
    path(
        "studios/<int:id>/",
        StudiosViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="studio-detail",
    ),
    path(
        "movies/<int:id>/",
        MoviesViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="movie-detail",
    ),
    path(
        "media-files/<int:id>/",
        MediaFileViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="media-file-detail",
    ),
    path(
        "movies/<int:movie_id>/recommendations/",
        movie_recommendations,
        name="movie-recommendations",
    ),
] + router.urls
