from typing import Final

from django.db import models
from core.settings import settings


class BaseRouter:
    """
    Класс, реализующий взаимодействие с несколькими БД
    в разных приложениях.

    Также используется для использования функций: unique и т.д.
    """

    route_app_label: Final[str] = "panel"
    default_database: Final[str] = "default"
    external_database = settings.DB_BACKEND_NAME

    def db_for_read(self, model: models.Model, **hints):
        if model._meta.app_label == self.route_app_label:
            return self.external_database
        return self.default_database

    def db_for_write(self, model: models.Model, **hints):
        if model._meta.app_label == self.route_app_label:
            return self.external_database
        return self.default_database

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {
            self.external_database,
        }
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
