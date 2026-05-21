import uuid
from django.db import models
from django.utils import timezone


# custom queries for soft delete functionality
class BaseQuerySet(models.QuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def restore(self):
        return self.update(deleted_at=None)


# custom manager to use the custom queryset and provide additional methods for soft delete functionality
class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    def get_queryset(self):
        return super().get_queryset().alive()

    def all_with_deleted(self):
        return super().get_queryset()

    def only_deleted(self):
        return super().get_queryset().dead()


# abstract base model that includes common fields and methods for soft delete functionality
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = BaseManager()
    all_objects = models.Manager.from_queryset(BaseQuerySet)()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    @property
    def is_deleted(self):
        return self.deleted_at is not None
