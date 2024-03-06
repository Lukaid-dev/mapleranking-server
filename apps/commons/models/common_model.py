from django.db import models


class CommonModel(models.Model):
    """Common Model Definition"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
