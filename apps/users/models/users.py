from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        default_related_name = "users"

    id = models.AutoField(primary_key=True)
    # firebase auth uuid
    uid = models.CharField(
        max_length=150,
        blank=False,
        default="",
    )
    # from firebase auth
    name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default="",
    )
    firebase_picture = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        default="",
    )

    first_name = None
    last_name = None

    # delete option
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # deleted_reason = models.ForeignKey(
    #     "users.UserDeleteReason",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return f"{self.id}_{self.username}"
