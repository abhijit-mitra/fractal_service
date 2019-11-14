from django.db import models


class BaseModel(models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Buckets(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        managed = True


class ToDOs(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    done = models.BooleanField(default=False)
    bucket = models.ForeignKey(Buckets, models.CASCADE, null=False, blank=False)

    class Meta:
        managed = True
