from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    DirectorsViewSet,
    StudiosViewSet,
    MoviesViewSet,
    MediaFileViewSet,
    movie_recommendations,
)

router = DefaultRouter()
router.register(r"directors", DirectorsViewSet, basename='directors')
router.register(r"studios", StudiosViewSet, basename='studios')
router.register(r"movies", MoviesViewSet, basename='movies')
router.register(r"media-files", MediaFileViewSet, basename='media-files')

urlpatterns = [
    path(
        "movies/<int:movie_id>/recommendations/",
        movie_recommendations,
        name="movie-recommendations",
    ),
] + router.urls
