from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel, BaseTitle

User = get_user_model()


class Location(BaseModel):
    """Location."""

    name = models.CharField(max_length=256, verbose_name="Place name")

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name


class Category(BaseModel, BaseTitle):
    """Category."""

    description = models.TextField(verbose_name="Description")
    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        help_text="URL page identifier; letters, numbers, hyphens, and underscores are allowed.",
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Post(BaseModel, BaseTitle):
    """Post."""

    text = models.TextField(verbose_name="Text")
    pub_date = models.DateTimeField(
        verbose_name="Publication date and time",
        help_text="Set a future date and time to schedule the post.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_posts",
        verbose_name="Post author",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="loc_posts",
        blank=True,
        verbose_name="Location",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="cat_posts",
        verbose_name="Category",
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
