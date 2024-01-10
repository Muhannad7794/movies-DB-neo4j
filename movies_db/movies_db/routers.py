class Neo4jRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to default.
        """
        if model._meta.app_label in ["auth", "contenttypes", "sessions", "admin"]:
            return "default"
        return "neo4j"

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to default.
        """
        if model._meta.app_label in ["auth", "contenttypes", "sessions", "admin"]:
            return "default"
        return "neo4j"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Do not allow relations involving the Neo4j database.
        """
        if obj1._state.db == "neo4j" or obj2._state.db == "neo4j":
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the 'default'
        database.
        """
        if app_label in ["auth", "contenttypes", "sessions", "admin"]:
            return db == "default"
        return False
