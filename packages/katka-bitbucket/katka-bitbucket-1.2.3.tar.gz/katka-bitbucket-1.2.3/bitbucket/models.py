from django.db import models

from encrypted_model_fields.fields import EncryptedCharField


class KatkaProject(models.Model):
    project_id = models.UUIDField(unique=True, null=False, blank=False)
    oauth_access_token = EncryptedCharField(max_length=100, null=True, blank=True)
