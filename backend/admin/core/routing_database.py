from django.db.models.base import ModelBase


class BaseRouter:
    route_app_label = "panel"

    def db_for_read(self, model: ModelBase, **hints):
        if model._meta.app_label == self.route_app_label:
            return "handbook"
        return "default"

    def db_for_write(self, model: ModelBase, **hints):
        if model._meta.app_label == self.route_app_label:
            return "handbook"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {
            "handbook",
        }
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
