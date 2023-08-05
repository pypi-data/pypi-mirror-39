from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.conf import settings


UserModel = get_user_model()
# Create your models here.

class UserSettings(models.Model):
    key = models.CharField(max_length=250)
    value = JSONField()
    user = models.ForeignKey(UserModel,
                             db_column="user_id",
                             editable=True,
                             on_delete=models.SET_NULL,
                             blank=True,
                             default=None,
                             null=True
                             )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_createdby',
        editable=False, null=True, blank=True,
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_modifiedby',
        null=True, blank=True, editable=False,
        on_delete=models.SET_NULL
    )
    is_archive = models.BooleanField(default=False, editable=False)

    def archive(self, user=None):
        update_fields = ['is_archive']

        if user:
            self.modified_by = user
            update_fields.append('modified_by')

        self.is_archive = True
        self.save(update_fields=update_fields)

    def __str__(self):
        return "Key: {}, Value: {}".format(self.key, self.value)

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "user": self.user.id if self.user is not None else None,
            "created_by": self.created_by.id if self.created_by is not None else None,
            "modified_by": self.modified_by.id if self.modified_by is not None else None,
        }
    objects = models.Manager()
