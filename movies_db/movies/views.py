from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .services.recommend import TMDBService
from .serializers import (
    DirectorsSerializer,
    StudiosSerializer,
    MoviesSerializer,
    MediaFilesSerializer,
)
from .models import Director, Studio, Movie, MediaFile


class DirectorsViewSet(viewsets.ViewSet):
    serializer_class = DirectorsSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search", description="Search Directors", required=False, type=str
            ),
            OpenApiParameter(
                name="order", description="Order by", required=False, type=str
            ),
        ]
    )
    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "director_name")

        queryset = Director.nodes
        queryset_list = list(queryset)

        # Implementing custom search logic
        if search:
            queryset_list = [
                director
                for director in queryset_list
                if search.lower() in director.director_name.lower()
                or search.lower() in director.nationality.lower()
                or search.lower() in director.awards.lower()
                or search.lower() in director.director_best_movies.lower()
            ]

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["director_name", "director_date_of_birth"]:
                queryset_list.sort(
                    key=lambda x: getattr(x, order, None), reverse=reverse
                )

        serializer = DirectorsSerializer(queryset_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DirectorsSerializer(data=request.data)
        if serializer.is_valid():
            director = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DirectorsSerializer(director)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DirectorsSerializer(director, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DirectorsSerializer(director, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            director = Director.nodes.get(id=pk)
            director.delete()
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudiosViewSet(viewsets.ViewSet):
    serializer_class = StudiosSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search", description="Search Studios", required=False, type=str
            ),
            OpenApiParameter(
                name="order", description="Order by", required=False, type=str
            ),
        ]
    )
    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "name")

        queryset = Studio.nodes
        queryset_list = list(queryset)

        # Implementing custom search logic
        if search:
            queryset_list = [
                studio
                for studio in queryset_list
                if search.lower() in studio.name.lower()
                or search.lower() in studio.location.lower()
            ]

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["name", "founded"]:
                queryset_list.sort(
                    key=lambda x: getattr(x, order, None), reverse=reverse
                )

        serializer = StudiosSerializer(queryset_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StudiosSerializer(data=request.data)
        if serializer.is_valid():
            studio = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudiosSerializer(studio)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudiosSerializer(studio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudiosSerializer(studio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            studio = Studio.nodes.get(id=pk)
            studio.delete()
        except Studio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesViewSet(viewsets.ViewSet):
    serializer_class = MoviesSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search", description="Search Movies", required=False, type=str
            ),
            OpenApiParameter(
                name="order", description="Order by", required=False, type=str
            ),
        ]
    )
    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "title")

        queryset = Movie.nodes
        queryset_list = list(queryset)

        # Implementing custom search logic
        if search:
            queryset_list = [
                movie
                for movie in queryset_list
                if search.lower() in movie.title.lower()
                or search.lower() in movie.genre.lower()
                # search with realease year. note that release year is an integer
                or search in str(movie.releaseYear)
                #search with credits score. note that credits_score is a float
                or search in str(movie.credits_score)
            ]

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["title", "releaseYear", "credits_score"]:
                queryset_list.sort(
                    key=lambda x: getattr(x, order, None), reverse=reverse
                )

        serializer = MoviesSerializer(queryset_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MoviesSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MoviesSerializer(movie)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MoviesSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MoviesSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            movie = Movie.nodes.get(id=pk)
            movie.delete()
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaFileViewSet(viewsets.ViewSet):
    serializer_class = MediaFilesSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search Media Files",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="order", description="Order by", required=False, type=str
            ),
        ]
    )
    def list(self, request):
        search = request.query_params.get("search")
        order = request.query_params.get("order", "title")

        queryset = MediaFile.nodes
        queryset_list = list(queryset)

        # Implementing custom search logic
        if search:
            queryset_list = [
                media_file
                for media_file in queryset_list
                if search.lower() in media_file.movie.lower()
            ]

        # Implementing custom ordering logic
        if order:
            reverse = False
            if order.startswith("-"):
                reverse = True
                order = order[1:]
            if order in ["movie"]:
                queryset_list.sort(
                    key=lambda x: getattr(x, order, None), reverse=reverse
                )

        serializer = MediaFilesSerializer(queryset_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MediaFilesSerializer(data=request.data)
        if serializer.is_valid():
            media_file = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MediaFilesSerializer(media_file)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MediaFilesSerializer(media_file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MediaFilesSerializer(media_file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            media_file = MediaFile.nodes.get(id=pk)
            media_file.delete()
        except MediaFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
