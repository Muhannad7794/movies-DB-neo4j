from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from .services.recommend import TMDBService
from .serializers import (
    DirectorsSerializer,
    StudiosSerializer,
    MoviesSerializer,
    MediaFilesSerializer,
)
from .models import Director, Studio, Movie, MediaFile


class DirectorsViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting directors.
    """

    serializer_class = DirectorsSerializer

    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "director_name")  # Default ordering

        queryset = Director.nodes

        # Implementing custom search logic
        if search:
            queryset = [
                director
                for director in queryset
                if search.lower() in director.director_name.lower()
                or search.lower() in director.nationality.lower()
                or search.lower() in director.awards.lower()
            ]

        # Convert NodeSet to a list for sorting
        queryset_list = list(queryset)

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["director_name", "director_date_of_birth"]:
                queryset_list.sort(key=lambda x: getattr(x, order), reverse=reverse)

        serializer = DirectorsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DirectorsSerializer(director)
        return Response(serializer.data)

    # Implementing custom delete logic
    def destroy(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudiosViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting studios.
    """

    serializer_class = StudiosSerializer

    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "name")  # Default ordering

        queryset = Studio.nodes

        # Implementing custom search logic
        if search:
            queryset = [
                studio
                for studio in queryset
                if search.lower() in studio.name.lower()
                or search.lower() in studio.location.lower()
            ]
        # Convert NodeSet to a list for sorting
        queryset_list = list(queryset)

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["name", "founded"]:
                queryset_list.sort(key=lambda x: getattr(x, order), reverse=reverse)

        serializer = StudiosSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StudiosSerializer(studio)
        return Response(serializer.data)

    # Implementing custom delete logic
    def destroy(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        studio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting movies.
    """

    serializer_class = MoviesSerializer

    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "title")  # Default ordering

        queryset = Movie.nodes

        # Implementing custom search logic
        if search:
            queryset = [
                movie
                for movie in queryset
                if search.lower() in movie.title.lower()
                or search.lower() in movie.genre.lower()
            ]
        # Convert NodeSet to a list for sorting
        queryset_list = list(queryset)

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["title", "release_year", "credits_score"]:
                queryset_list.sort(key=lambda x: getattr(x, order), reverse=reverse)

        serializer = MoviesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MoviesSerializer(movie)
        return Response(serializer.data)

    # Implementing custom delete logic
    def destroy(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaFileViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting media files.
    """

    serializer_class = MediaFilesSerializer

    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "url")  # Default ordering

        queryset = MediaFile.nodes

        # Implementing custom search logic
        if search:
            queryset = [
                media_file
                for media_file in queryset
                if search.lower() in media_file.url.lower()
            ]
        # Convert NodeSet to a list for sorting
        queryset_list = list(queryset)

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["url"]:
                queryset_list.sort(key=lambda x: getattr(x, order), reverse=reverse)

        serializer = MediaFilesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MediaFilesSerializer(media_file)
        return Response(serializer.data)

    # Implementing custom delete logic
    def destroy(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        media_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = MediaFilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def movie_recommendations(request, movie_id):
    try:
        movie = Movie.nodes.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)

    tmdb_service = TMDBService()
    tmdb_id = tmdb_service.search_movie(movie.title)
    if tmdb_id:
        recommendations = tmdb_service.get_similar_movies(tmdb_id)
        return Response(recommendations)
    else:
        return Response({"error": "Movie not found in TMDB"}, status=404)
