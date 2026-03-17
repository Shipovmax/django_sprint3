from django.contrib import admin

from .models import Location, Category, Post

admin.site.empty_value_display = "Not set"


def get_all_fields(model):
    """Return the full list of model fields."""
    return model._meta.get_fields()


class BlogAdmin(admin.ModelAdmin):
    """Shared admin configuration for the blog app."""

    list_editable = ("is_published",)


@admin.register(Post)
class PostAdmin(BlogAdmin):
    """Admin configuration for posts."""

    list_display = [
        field.name
        for field in get_all_fields(Post)
        if field.name not in ("id", "text")
    ]
    list_display_links = ("title",)
    search_fields = (
        "title",
        "text",
    )
    list_filter = (
        "is_published",
        "category",
        "location",
        "author",
    )


@admin.register(Category)
class CategoryAdmin(BlogAdmin):
    """Admin configuration for categories."""

    list_display = (
        "title",
        "is_published",
        "created_at",
        "slug",
    )


@admin.register(Location)
class LocationAdmin(BlogAdmin):
    """Admin configuration for locations."""

    list_display = (
        "name",
        "is_published",
        "created_at",
    )
