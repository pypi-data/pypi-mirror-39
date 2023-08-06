import uuid

from django.db import models
from simple_history.models import HistoricalRecords as SimpleHistoricalRecords


class SerializableModelManager(models.Manager):

    def get_by_natural_key(self, history_id):
        return self.get(history_id=history_id)


class SerializableModel(models.Model):

    objects = SerializableModelManager()

    def natural_key(self):
        return (self.history_id, )

    class Meta:
        abstract = True


class HistoricalRecords(SimpleHistoricalRecords):

    """HistoricalRecords that uses a UUID primary key
    and has a natural key method available for serialization.
    """

    model_cls = SerializableModel

    def __init__(self, **kwargs):
        """Defaults use of UUIDField instead of AutoField.
        """
        kwargs.update(bases=(self.model_cls, ))
        kwargs.update(history_id_field=models.UUIDField(default=uuid.uuid4))
        super().__init__(**kwargs)

    def get_extra_fields(self, model, fields):
        """Overridden to add natural key.
        """
        extra_fields = super().get_extra_fields(model, fields)
        extra_fields.update({'natural_key': lambda x: (x.history_id, )})
        return extra_fields
