from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty,
    FloatProperty,
    DateProperty,
    UniqueIdProperty,
)


# Neo4j model for Media Files
class MediaFile(StructuredNode):
    url = StringProperty(unique_index=True, required=True)
    # relationships to different nodes 
    movie = RelationshipFrom("Movie", "HAS_POSTER")
    director = RelationshipFrom("Director", "HAS_IMAGE")
    studio = RelationshipFrom("Studio", "HAS_LOGO")


# Neo4j model for Movies
class Movie(StructuredNode):
    title = StringProperty(unique_index=True, required=True)
    genre = StringProperty()
    releaseYear = IntegerProperty()
    credits_score = FloatProperty()
    # Relationships
    directed_by = RelationshipTo("Director", "DIRECTED_BY")
    produced_by = RelationshipTo("Studio", "PRODUCED_BY")
    poster = RelationshipTo("MediaFile", "HAS_POSTER")


# Neo4j model for Directors
class Director(StructuredNode):
    director_name = StringProperty(unique_index=True, required=True)
    nationality = StringProperty()
    director_date_of_birth = DateProperty()
    director_best_movies = StringProperty()
    awards = StringProperty()
    # Relationship
    directed_movies = RelationshipFrom("Movie", "DIRECTED_BY")
    image = RelationshipTo("MediaFile", "HAS_IMAGE")


# Neo4j model for Studios
class Studio(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    founded = IntegerProperty()
    location = StringProperty()
    # Relationship
    produced_movies = RelationshipFrom("Movie", "PRODUCED_BY")
    logo = RelationshipTo("MediaFile", "HAS_LOGO")
