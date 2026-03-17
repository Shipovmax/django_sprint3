import importlib

import pytest
from django.apps import apps
from django.conf import settings


def test_english_localization():
    assert hasattr(settings, 'LANGUAGE_CODE'), (
        'The application settings do not define the `LANGUAGE_CODE` key.'
    )
    assert settings.LANGUAGE_CODE == 'en-us', (
        'The `LANGUAGE_CODE` setting must be set to `en-us`.'
    )


def test_blog_in_english():
    applications = apps.get_app_configs()
    blog_app = list(filter(lambda x: x.name == 'blog', applications))[0]
    assert blog_app.verbose_name == 'Blog', (
        'The `Blog` application is not localized in English.'
    )


@pytest.mark.parametrize(('n_model', 'n_verbose', 'n_verbose_plural'), [
    ('Category', 'category', 'Categories'),
    ('Location', 'location', 'Locations'),
    ('Post', 'post', 'Posts'),
])
def test_models_translated(n_model, n_verbose, n_verbose_plural):
    models = apps.get_models()
    found_model = [
        model for model in models
        if model._meta.object_name == n_model
        and hasattr(model, 'Meta')
    ]
    assert found_model, (
        f'Ensure the `{n_model}` model defines a `Meta` subclass.'
    )
    found_model = found_model[0]
    assert found_model._meta.verbose_name == n_verbose, (
        f'Ensure the `{n_model}` model sets `verbose_name` as required.'
    )
    assert (
        found_model._meta.verbose_name_plural == n_verbose_plural
    ), (
        f'Ensure the `{n_model}` model sets `verbose_name_plural` as required.'
    )


@pytest.mark.parametrize(('n_model', 'param', 'n_verbose'), [
    ('Category', 'is_published', 'Published'),
    ('Category', 'title', 'Title'),
    ('Category', 'slug', 'Slug'),
    ('Category', 'description', 'Description'),
    ('Category', 'created_at', 'Created'),
    ('Location', 'name', 'Place name'),
    ('Location', 'created_at', 'Created'),
    ('Location', 'is_published', 'Published'),
    ('Post', 'pub_date', 'Publication date and time'),
    ('Post', 'text', 'Text'),
    ('Post', 'author', 'Post author'),
    ('Post', 'category', 'Category'),
    ('Post', 'location', 'Location'),
    ('Post', 'created_at', 'Created'),
    ('Post', 'is_published', 'Published'),
])
def test_models_params_translate(n_model, param, n_verbose):
    module = importlib.import_module('blog.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.verbose_name == n_verbose, (
        f'Ensure the `{n_model}` model sets `verbose_name` correctly '
        f'for the `{param}` field.'
    )


@pytest.mark.parametrize(('n_model', 'param', 'text'), [
    (
        'Category',
        'is_published',
        'Clear this checkbox to hide the entry.'
    ),
    (
        'Category',
        'slug',
        'URL page identifier; letters, numbers, hyphens, and underscores are allowed.'
    ),
    (
        'Post',
        'pub_date',
        'Set a future date and time to schedule the post.'
    ),
])
def test_help_text_translate(n_model, param, text):
    module = importlib.import_module('blog.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.help_text == text, (
        f'Ensure the `{n_model}` model sets `help_text` correctly '
        f'for the `{param}` field.'
    )
