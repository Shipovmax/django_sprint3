from django.db import models


class BaseModel(models.Model):
    """Base abstract model."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Published',
        help_text='Clear this checkbox to hide the entry.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created'
    )

    class Meta:
        abstract = True


class BaseTitle(models.Model):
    """Base abstract model with a title."""

    title = models.CharField(max_length=256, verbose_name='Title')

    class Meta:
        abstract = True
