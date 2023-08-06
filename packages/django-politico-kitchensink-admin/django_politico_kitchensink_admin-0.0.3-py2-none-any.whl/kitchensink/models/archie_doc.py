import uuid

from django.db import models

from foreignform.fields import JSONField


class ArchieDoc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        "Project title", max_length=250, help_text="A title for this doc"
    )
    doc_id = models.SlugField("Google Doc ID", help_text="Doc ID from URL")

    validation_schema = JSONField(
        blank=True, null=True, help_text="JSON Schema"
    )

    def __str__(self):
        return self.title
