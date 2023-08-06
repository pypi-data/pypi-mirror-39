from django.conf import settings


class UserRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to USER_DB.
        """
        if model._meta.app_label == 'auth':
            return settings.USER_DB
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to USER_DB.
        """
        if model._meta.app_label == 'auth':
            return settings.USER_DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if any([obj1._meta.app_label == 'auth',
                obj2._meta.app_label == 'auth']):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the USER_DB
        database.
        """
        if app_label == 'auth':
            return settings.USER_DB
        return None
