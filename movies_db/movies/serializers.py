from rest_framework import serializers
from .models import Movie, MediaFile, Director, Studio


class DirectorsSerializer(serializers.Serializer):
    director_name = serializers.CharField(max_length=100)
    nationality = serializers.CharField(max_length=100)
    director_date_of_birth = serializers.DateField()
    director_best_movies = serializers.CharField(max_length=215)
    awards = serializers.CharField(max_length=100)
    picture_url = serializers.SerializerMethodField()

    def get_picture_url(self, obj):
        if obj.image.single():
            return obj.image.single().url
        return None

    def create(self, validated_data):
        return Director(**validated_data).save()

    def update(self, instance, validated_data):
        instance.director_name = validated_data.get(
            "director_name", instance.director_name
        )
        instance.nationality = validated_data.get("nationality", instance.nationality)
        instance.director_date_of_birth = validated_data.get(
            "director_date_of_birth", instance.director_date_of_birth
        )
        instance.director_best_movies = validated_data.get(
            "director_best_movies", instance.director_best_movies
        )
        instance.awards = validated_data.get("awards", instance.awards)
        instance.picture_url = validated_data.get("picture_url", instance.picture_url)

        instance.save()
        return instance


class StudiosSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    founded = serializers.IntegerField()
    location = serializers.CharField(max_length=100)
    picture_url = serializers.SerializerMethodField()

    def get_picture_url(self, obj):
        if obj.logo.single():
            return obj.logo.single().url
        return None

    def create(self, validated_data):
        return Studio(**validated_data).save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.founded = validated_data.get("founded", instance.founded)
        instance.location = validated_data.get("location", instance.location)
        instance.picture_url = validated_data.get("picture_url", instance.picture_url)
        instance.save()
        return instance


class MoviesSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=100)
    releaseYear = serializers.IntegerField()
    credits_score = serializers.FloatField()
    director = DirectorsSerializer(read_only=True)
    studio = StudiosSerializer(read_only=True)
    poster_url = serializers.SerializerMethodField()

    def get_poster_url(self, obj):
        if obj.poster.single():
            return obj.poster.single().url
        return None

    def create(self, validated_data):
        return Movie(**validated_data).save()

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.genre = validated_data.get("genre", instance.genre)
        instance.release_year = validated_data.get(
            "release_year", instance.release_year
        )
        instance.credits_score = validated_data.get(
            "credits_score", instance.credits_score
        )
        instance.director = validated_data.get("director", instance.director)
        instance.studio = validated_data.get("studio", instance.studio)
        instance.poster_url = validated_data.get("poster_url", instance.poster_url)

        instance.save()
        return instance


class MediaFilesSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return MediaFile(**validated_data).save()

    def update(self, instance, validated_data):
        instance.url = validated_data.get("url", instance.url)
        instance.save()
        return instance
