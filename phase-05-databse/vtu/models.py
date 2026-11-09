from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user_id = models.AutoField(primary_key=True)

    bio = models.TextField(null=True, blank=True, default='bio')
    phone = models.TextField(null=True,  blank=True, unique=True)
    created_at = models.DateTimeField(null=True,  blank=True, default=timezone.now)
    name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "vtu_profile"

        indexes = [  # noqa: RUF012
            models.Index(fields=["name"], name="profile_name_index")
        ]


